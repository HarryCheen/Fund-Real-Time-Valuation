import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { sentimentApi } from '@/api';
import type { EconomicEventItem, EconomicEventsData, WeiboSentimentItem, WeiboSentimentData } from '@/types';
import { ApiError } from '@/api';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

const friendlyErrorMessages: Record<string, string> = {
  'NETWORK_ERROR': '网络连接失败，请检查网络设置',
  '请求参数验证失败': '请求参数错误，请检查输入',
  'Internal Server Error': '服务器暂时繁忙，请稍后重试',
  'timeout': '请求超时，请检查网络连接',
  '503': '服务暂时不可用',
};

export const useSentimentStore = defineStore('sentiment', () => {
  // Economic Events State
  const economicEvents = ref<EconomicEventItem[]>([]);
  const economicLoading = ref(false);
  const economicError = ref<string | null>(null);

  // Weibo Sentiment State
  const weiboSentiment = ref<WeiboSentimentItem[]>([]);
  const weiboLoading = ref(false);
  const weiboError = ref<string | null>(null);

  // Common State
  const lastUpdated = ref<string | null>(null);
  const selectedDate = ref<string>('');
  const selectedPeriod = ref<string>('12h');
  const showImportantOnly = ref(false);
  const retryCount = ref(0);
  const maxRetries = 2;

  function getFriendlyErrorMessage(err: unknown): string {
    if (err instanceof ApiError) {
      return friendlyErrorMessages[err.message] || err.message || '获取数据失败';
    }
    if (err instanceof Error) {
      return friendlyErrorMessages[err.message] || err.message || '获取数据失败';
    }
    return '获取数据失败';
  }

  // Filtered events based on importance
  const filteredEvents = computed(() => {
    if (showImportantOnly.value) {
      return economicEvents.value.filter(e => e.重要性 >= 2);
    }
    return economicEvents.value;
  });

  // Group events by time
  const eventsByTime = computed(() => {
    const grouped: Record<string, EconomicEventItem[]> = {};
    for (const event of filteredEvents.value) {
      const time = event.时间 || '未知';
      if (!grouped[time]) {
        grouped[time] = [];
      }
      grouped[time].push(event);
    }
    return grouped;
  });

  // Get sorted time keys
  const sortedTimeKeys = computed(() => {
    return Object.keys(eventsByTime.value).sort();
  });

  async function fetchEconomicEvents(date?: string, options: { showError?: boolean; retries?: number } = {}) {
    const retries = options.retries ?? maxRetries;
    const showError = options.showError ?? true;
    const targetDate = date || selectedDate.value || getTodayDate();

    economicLoading.value = true;
    economicError.value = null;
    retryCount.value = 0;

    let lastError: unknown;

    for (let attempt = 0; attempt <= retries; attempt++) {
      retryCount.value = attempt;
      try {
        const response: EconomicEventsData = await sentimentApi.getEconomicEvents(targetDate);
        economicEvents.value = response.events || [];
        selectedDate.value = targetDate;
        lastUpdated.value = new Date().toLocaleTimeString();
        return;
      } catch (err) {
        lastError = err;
        console.error(`[SentimentStore] fetchEconomicEvents attempt ${attempt + 1} error:`, err);

        if (attempt < retries) {
          await delay(1000 * (attempt + 1));
          continue;
        }
        break;
      }
    }

    economicError.value = getFriendlyErrorMessage(lastError);
    if (showError) {
      console.error('[SentimentStore] fetchEconomicEvents failed:', economicError.value);
    }
    economicLoading.value = false;
  }

  async function fetchWeiboSentiment(period: string = '12h', options: { showError?: boolean; retries?: number } = {}) {
    const retries = options.retries ?? maxRetries;
    const showError = options.showError ?? true;

    weiboLoading.value = true;
    weiboError.value = null;
    retryCount.value = 0;

    let lastError: unknown;

    for (let attempt = 0; attempt <= retries; attempt++) {
      retryCount.value = attempt;
      try {
        const response: WeiboSentimentData = await sentimentApi.getWeiboSentiment(period);
        weiboSentiment.value = response.sentiment || [];
        selectedPeriod.value = period;
        lastUpdated.value = new Date().toLocaleTimeString();
        return;
      } catch (err) {
        lastError = err;
        console.error(`[SentimentStore] fetchWeiboSentiment attempt ${attempt + 1} error:`, err);

        if (attempt < retries) {
          await delay(1000 * (attempt + 1));
          continue;
        }
        break;
      }
    }

    weiboError.value = getFriendlyErrorMessage(lastError);
    if (showError) {
      console.error('[SentimentStore] fetchWeiboSentiment failed:', weiboError.value);
    }
    weiboLoading.value = false;
  }

  function setDate(date: string) {
    selectedDate.value = date;
  }

  function setPeriod(period: string) {
    selectedPeriod.value = period;
  }

  function toggleImportantOnly() {
    showImportantOnly.value = !showImportantOnly.value;
  }

  async function retry() {
    if (economicEvents.value.length === 0) {
      await fetchEconomicEvents();
    }
  }

  return {
    // Economic Events
    economicEvents,
    economicLoading,
    economicError,
    filteredEvents,
    eventsByTime,
    sortedTimeKeys,

    // Weibo Sentiment
    weiboSentiment,
    weiboLoading,
    weiboError,

    // Common
    lastUpdated,
    selectedDate,
    selectedPeriod,
    showImportantOnly,

    // Actions
    fetchEconomicEvents,
    fetchWeiboSentiment,
    setDate,
    setPeriod,
    toggleImportantOnly,
    retry,
  };
}, {
  persist: {
    key: 'sentiment-store',
    pick: ['selectedDate', 'selectedPeriod', 'showImportantOnly'],
  },
});

function getTodayDate(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}${month}${day}`;
}
