import { useEffect, useState } from 'react';
import { supabase } from '../../lib/supabase';
import { Ticket } from '../../types';
import TicketCard from './TicketCard';

export default function TicketList() {
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchTickets();

        // Subscribe to realtime changes
        const channel = supabase
            .channel('schema-db-changes')
            .on(
                'postgres_changes',
                {
                    event: '*', // Listen to INSERT, UPDATE, DELETE
                    schema: 'public',
                    table: 'tickets',
                },
                (payload) => {
                    console.log('Realtime update:', payload);
                    if (payload.eventType === 'INSERT') {
                        setTickets((prev) => [payload.new as Ticket, ...prev]);
                    } else if (payload.eventType === 'UPDATE') {
                        setTickets((prev) =>
                            prev.map((t) => (t.id === payload.new.id ? (payload.new as Ticket) : t))
                        );
                    } else if (payload.eventType === 'DELETE') {
                        setTickets((prev) => prev.filter((t) => t.id !== payload.old.id));
                    }
                }
            )
            .subscribe();

        return () => {
            supabase.removeChannel(channel);
        };
    }, []);

    const fetchTickets = async () => {
        try {
            const { data, error } = await supabase
                .from('tickets')
                .select('*')
                .order('created_at', { ascending: false });

            if (error) {
                console.error('Error fetching tickets:', error);
            } else {
                setTickets(data || []);
            }
        } catch (err) {
            console.error('Unexpected error:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[...Array(6)].map((_, i) => (
                    <div key={i} className="h-48 rounded-xl bg-slate-800/50 border border-slate-700 animate-pulse"></div>
                ))}
            </div>
        );
    }

    if (tickets.length === 0) {
        return (
            <div className="text-center py-20 border-2 border-dashed border-slate-800 rounded-xl">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-slate-800 mb-4">
                    <svg className="w-8 h-8 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                    </svg>
                </div>
                <h3 className="text-lg font-medium text-slate-300">No tickets yet</h3>
                <p className="text-slate-500 mt-1">Waiting for incoming support requests...</p>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {tickets.map((ticket) => (
                <TicketCard key={ticket.id} ticket={ticket} />
            ))}
        </div>
    );
}
