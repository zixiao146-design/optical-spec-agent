import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import { dictionaries } from "./index";
import { LANGUAGE_STORAGE_KEY, type AgentStudioLanguage, type I18nContextValue } from "./types";

function isSupportedLanguage(value: string | null): value is AgentStudioLanguage {
  return value === "en" || value === "zh-CN";
}

function detectInitialLanguage(): AgentStudioLanguage {
  if (typeof window === "undefined") return "en";
  const stored = window.localStorage.getItem(LANGUAGE_STORAGE_KEY);
  if (isSupportedLanguage(stored)) return stored;
  const browserLanguage = window.navigator.language || "";
  return browserLanguage.toLowerCase().startsWith("zh") ? "zh-CN" : "en";
}

const I18nContext = createContext<I18nContextValue | undefined>(undefined);

interface LanguageProviderProps {
  children: ReactNode;
}

export function LanguageProvider({ children }: LanguageProviderProps) {
  const [language, setLanguageState] = useState<AgentStudioLanguage>(detectInitialLanguage);

  function setLanguage(nextLanguage: AgentStudioLanguage) {
    setLanguageState(nextLanguage);
    window.localStorage.setItem(LANGUAGE_STORAGE_KEY, nextLanguage);
  }

  const value = useMemo<I18nContextValue>(() => {
    const dictionary = dictionaries[language];
    return {
      language,
      setLanguage,
      t: (key: string) => dictionary[key] || dictionaries.en[key] || key,
    };
  }, [language]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(): I18nContextValue {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error("useI18n must be used inside LanguageProvider");
  }
  return context;
}
