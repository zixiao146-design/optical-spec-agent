import { en } from "./en";
import type { AgentStudioLanguage, I18nDictionary } from "./types";
import { zhCN } from "./zhCN";

export const dictionaries: Record<AgentStudioLanguage, I18nDictionary> = {
  en,
  "zh-CN": zhCN,
};

export { en, zhCN };
export type { AgentStudioLanguage, I18nContextValue, I18nDictionary } from "./types";
export { LANGUAGE_STORAGE_KEY } from "./types";
