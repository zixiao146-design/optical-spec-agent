interface DemoModeBannerProps {
  message?: string;
}

export function DemoModeBanner({ message }: DemoModeBannerProps) {
  return (
    <aside className="demo-mode-banner" aria-live="polite">
      <strong>Demo fixture loaded</strong>
      <span>{message || "Not live validation until submitted to the local API."}</span>
    </aside>
  );
}
