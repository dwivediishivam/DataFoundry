'use client';

import { useState } from 'react';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import type { Startup } from '@/lib/types';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Loader2, Save } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';

const formSchema = z.object({
  marketSize: z.number().min(0).max(100),
  teamExperience: z.number().min(0).max(100),
  traction: z.number().min(0).max(100),
});

type DataTabProps = {
  data: Startup['data'];
  weightages: Startup['weightages'];
};

export function DataTab({ data, weightages }: DataTabProps) {
  const [isSaving, setIsSaving] = useState(false);
  const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      marketSize: weightages.marketSize,
      teamExperience: weightages.teamExperience,
      traction: weightages.traction,
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    setIsSaving(true);
    console.log(values);
    setTimeout(() => {
      setIsSaving(false);
      toast({
        title: 'Weightages Saved',
        description:
          'Your preferences have been updated. You can now regenerate the deal note.',
      });
    }, 1000);
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>DATA FOUNDRY</CardTitle>
          <CardDescription>
            This is the source data used for the AI analysis.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="pitchDeck">Pitch Deck Summary</Label>
            <Textarea id="pitchDeck" readOnly value={data.pitchDeck} rows={5} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="founderUpdates">Founder Updates</Label>
            <Textarea
              id="founderUpdates"
              readOnly
              value={data.founderUpdates}
              rows={5}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="publicData">Public Data</Label>
            <Textarea
              id="publicData"
              readOnly
              value={data.publicData}
              rows={5}
            />
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Customizable Weightages</CardTitle>
          <CardDescription>
            Adjust the importance of different factors for the investment
            recommendation.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <FormField
                control={form.control}
                name="marketSize"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex justify-between">
                      <span>Market Size</span>
                      <span className="text-muted-foreground">{field.value}%</span>
                    </FormLabel>
                    <FormControl>
                      <Slider
                        defaultValue={[field.value]}
                        onValueChange={(value) => field.onChange(value[0])}
                        max={100}
                        step={1}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="teamExperience"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex justify-between">
                      <span>Team Experience</span>
                      <span className="text-muted-foreground">{field.value}%</span>
                    </FormLabel>
                    <FormControl>
                      <Slider
                        defaultValue={[field.value]}
                        onValueChange={(value) => field.onChange(value[0])}
                        max={100}
                        step={1}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="traction"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="flex justify-between">
                      <span>Traction</span>
                      <span className="text-muted-foreground">{field.value}%</span>
                    </FormLabel>
                    <FormControl>
                      <Slider
                        defaultValue={[field.value]}
                        onValueChange={(value) => field.onChange(value[0])}
                        max={100}
                        step={1}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full" disabled={isSaving}>
                {isSaving ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Save className="mr-2 h-4 w-4" />
                )}
                Save Weights
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
