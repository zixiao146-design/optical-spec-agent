export type AgentStudioLanguage = "en" | "zh-CN";

export type I18nDictionary = Record<string, string>;

export interface I18nContextValue {
  language: AgentStudioLanguage;
  setLanguage: (language: AgentStudioLanguage) => void;
  t: (key: string) => string;
}

export const LANGUAGE_STORAGE_KEY = "agent-studio-language";
