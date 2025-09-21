import { Header } from '@/components/layout/header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function SettingsPage() {
  return (
    <div className="flex flex-col h-full">
      <Header
        title="Settings"
        description="Manage your account and preferences."
      />
      <div className="flex-1 p-6 pt-0">
        <Card>
          <CardHeader>
            <CardTitle>Preferences</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Settings and preferences will be available here in a future update.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
