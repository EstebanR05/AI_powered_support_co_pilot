export type TicketCategory = 'Technical' | 'Billing' | 'Sales' | 'Other';
export type TicketSentiment = 'Positive' | 'Neutral' | 'Negative';

export interface Ticket {
    id: string;
    created_at: string;
    description: string;
    category: TicketCategory | null;
    sentiment: TicketSentiment | null;
    processed: boolean;
}
