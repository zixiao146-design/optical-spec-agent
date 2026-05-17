import { useI18n } from "../i18n/useI18n";

interface DemoModeBannerProps {
  message?: string;
}

export function DemoModeBanner({ message }: DemoModeBannerProps) {
  const { t } = useI18n();
  return (
    <aside className="demo-mode-banner" aria-live="polite">
      <strong>{t("state.demoLoadedTitle")}</strong>
      <span>{message || t("state.demoLoadedMessage")}</span>
    </aside>
  );
}
