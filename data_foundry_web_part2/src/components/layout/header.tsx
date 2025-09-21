import type { ReactNode } from 'react';

type HeaderProps = {
  title: string;
  description?: string;
  actions?: ReactNode;
};

export function Header({ title, description, actions }: HeaderProps) {
  return (
    <header className="flex items-center justify-between p-6">
      <div className="grid gap-1">
        <h1 className="text-2xl font-bold tracking-tight md:text-3xl">{title}</h1>
        {description && <p className="text-muted-foreground">{description}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </header>
  );
}
