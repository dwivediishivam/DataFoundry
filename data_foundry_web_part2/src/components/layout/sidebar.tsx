'use client';

import {
  Sidebar,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
  SidebarTrigger,
} from '@/components/ui/sidebar';
import {
  Settings,
  LayoutDashboard,
  Rocket,
  ChevronLeft,
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';

export function AppSidebar() {
  const pathname = usePathname();
  const isActive = (path: string) => {
    if (path === '/') return pathname === '/';
    return pathname.startsWith(path);
  };

  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-2">
          <div className="bg-primary text-primary-foreground rounded-lg p-2 flex items-center justify-center">
            <Rocket className="w-6 h-6" />
          </div>
          <h1 className="text-xl font-semibold">Investor AI</h1>
        </div>
      </SidebarHeader>
      <SidebarMenu>
        <SidebarMenuItem>
          <Link href="/" passHref>
            <SidebarMenuButton
              isActive={isActive('/')}
              icon={<LayoutDashboard />}
              tooltip="Dashboard"
            >
              Dashboard
            </SidebarMenuButton>
          </Link>
        </SidebarMenuItem>
        <SidebarMenuItem>
          <Link href="/startups" passHref>
            <SidebarMenuButton
              isActive={isActive('/startups')}
              icon={<Rocket />}
              tooltip="Startups"
            >
              Startups
            </SidebarMenuButton>
          </Link>
        </SidebarMenuItem>
        <SidebarMenuItem>
          <Link href="/settings" passHref>
            <SidebarMenuButton
              isActive={isActive('/settings')}
              icon={<Settings />}
              tooltip="Settings"
            >
              Settings
            </SidebarMenuButton>
          </Link>
        </SidebarMenuItem>
      </SidebarMenu>
      <SidebarFooter>
        <SidebarTrigger>
          <Button variant="ghost" size="icon">
            <ChevronLeft />
          </Button>
        </SidebarTrigger>
      </SidebarFooter>
    </Sidebar>
  );
}
