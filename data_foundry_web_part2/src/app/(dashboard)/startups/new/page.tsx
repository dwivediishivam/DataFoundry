'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Header } from '@/components/layout/header';
import { ArrowLeft, Bot, Loader2 } from 'lucide-react';
import Link from 'next/link';
import { useToast } from '@/hooks/use-toast';
import { analyzeStartup } from './actions';

const formSchema = z.object({
  name: z.string().min(1, 'Company name is required'),
  description: z.string().min(1, 'Description is required'),
  pitchDeck: z.any().optional(),
});

export default function NewStartupPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();
  const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      description: '',
    },
  });
  
  const fileRef = form.register("pitchDeck");

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsSubmitting(true);
    
    const formData = new FormData();
    formData.append('name', values.name);
    formData.append('description', values.description);
    if (values.pitchDeck?.[0]) {
        formData.append('pitchDeck', values.pitchDeck[0]);
    }
    
    try {
        await analyzeStartup(formData);
        toast({
            title: 'Analysis Complete',
            description: `${values.name} has been analyzed and added to your dashboard.`,
        });
        router.push('/');
    } catch (error) {
        console.error(error);
        toast({
            title: 'Analysis Failed',
            description: 'Something went wrong. Please try again.',
            variant: 'destructive',
        });
    } finally {
        setIsSubmitting(false);
    }
  }

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Analyze New Startup"
        description="Enter the details below to begin the AI analysis."
        actions={
          <Link href="/" passHref>
            <Button variant="outline">
              <ArrowLeft className="mr-2" />
              Back to Dashboard
            </Button>
          </Link>
        }
      />
      <div className="flex-1 p-6 pt-0">
        <Card>
          <CardHeader>
            <CardTitle>Startup Details</CardTitle>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-6"
              >
                <div className="grid gap-6 md:grid-cols-2">
                  <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Company Name</FormLabel>
                        <FormControl>
                          <Input placeholder="e.g. Innovatech" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="description"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>One-line Description</FormLabel>
                        <FormControl>
                          <Input
                            placeholder="e.g. AI-driven enterprise solutions"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                 <div className="grid gap-6 md:grid-cols-2">
                    <FormField
                    control={form.control}
                    name="pitchDeck"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel>Pitch Deck</FormLabel>
                        <FormControl>
                            <Input type="file" {...fileRef} />
                        </FormControl>
                        <FormMessage />
                        </FormItem>
                    )}
                    />
                </div>

                <Button type="submit" className="w-full" disabled={isSubmitting}>
                  {isSubmitting ? (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  ) : (
                    <Bot className="mr-2 h-4 w-4" />
                  )}
                  Analyze Startup
                </Button>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
