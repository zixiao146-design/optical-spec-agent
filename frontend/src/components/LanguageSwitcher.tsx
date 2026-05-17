import { useI18n } from "../i18n/useI18n";

export function LanguageSwitcher() {
  const { language, setLanguage, t } = useI18n();
  return (
    <div className="language-switcher" aria-label={t("language.label")}>
      <span>{t("language.label")}</span>
      <div role="group" aria-label={t("language.label")}>
        <button
          type="button"
          className={language === "en" ? "active" : ""}
          onClick={() => setLanguage("en")}
          aria-pressed={language === "en"}
          aria-label="English"
        >
          {t("language.english")}
        </button>
        <button
          type="button"
          className={language === "zh-CN" ? "active" : ""}
          onClick={() => setLanguage("zh-CN")}
          aria-pressed={language === "zh-CN"}
          aria-label="中文"
        >
          {t("language.chinese")}
        </button>
      </div>
    </div>
  );
}
