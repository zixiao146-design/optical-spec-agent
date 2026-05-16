interface BoundaryBadgeProps {
  children: string;
  tone?: "safe" | "notice" | "neutral";
}

export function BoundaryBadge({ children, tone = "safe" }: BoundaryBadgeProps) {
  return <span className={`boundary-badge boundary-badge-${tone}`}>{children}</span>;
}
