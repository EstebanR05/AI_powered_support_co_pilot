import { useState } from 'react';
import { Ticket } from '../../types';

interface TicketCardProps {
    ticket: Ticket;
}

export default function TicketCard({ ticket }: TicketCardProps) {
    const [processing, setProcessing] = useState(false);

    const handleProcess = async () => {
        setProcessing(true);
        try {
            // TODO: Replace with actual API call to Python Microservice
            const response = await fetch('http://localhost:8000/process-ticket', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ticket_id: ticket.id, text: ticket.description }),
            });

            if (!response.ok) throw new Error('Processing failed');

            // We don't need to manually update state here because the 
            // Supersbase Realtime subscription in the parent list will
            // catch the 'processed: true' update and re-render this card.
        } catch (error) {
            console.error('Error processing ticket:', error);
            alert('Failed to process ticket. Ensure the AI Service is running.');
        } finally {
            setProcessing(false);
        }
    };

    const getSentimentColor = (sentiment: string | null) => {
        switch (sentiment?.toLowerCase()) {
            case 'positive': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
            case 'negative': return 'bg-red-500/10 text-red-400 border-red-500/20';
            case 'neutral': return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
            default: return 'bg-slate-700/50 text-slate-400 border-slate-700';
        }
    };

    const getCategoryIcon = (category: string | null) => {
        switch (category?.toLowerCase()) {
            case 'technical': return '🔧';
            case 'billing': return '💳';
            case 'sales': return '💼';
            default: return '📝';
        }
    };

    return (
        <div className={`
      relative overflow-hidden rounded-xl border p-5 transition-all duration-300
      ${ticket.processed
                ? 'bg-slate-800/50 border-slate-700/50'
                : 'bg-slate-800 border-slate-700 shadow-lg hover:shadow-blue-500/5 hover:border-blue-500/30'
            }
    `}>
            <div className="flex justify-between items-start mb-3">
                <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-slate-500">{ticket.id.slice(0, 8)}</span>
                    {ticket.created_at && (
                        <span className="text-xs text-slate-500">
                            • {new Date(ticket.created_at).toLocaleTimeString()}
                        </span>
                    )}
                </div>

                {ticket.processed ? (
                    <div className="flex gap-2">
                        <span className={`text-xs px-2.5 py-1 rounded-full border flex items-center gap-1.5 ${getSentimentColor(ticket.sentiment)}`}>
                            <span>{ticket.sentiment}</span>
                        </span>
                        <span className="text-xs px-2.5 py-1 rounded-full bg-slate-700 border border-slate-600 text-slate-300 flex items-center gap-1.5">
                            <span>{getCategoryIcon(ticket.category)} {ticket.category}</span>
                        </span>
                    </div>
                ) : (
                    <span className="flex h-2 w-2 relative">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                    </span>
                )}
            </div>

            <p className="text-slate-300 text-sm leading-relaxed mb-4">
                {ticket.description}
            </p>

            <div className="flex items-center justify-end">
                {!ticket.processed ? (
                    <button
                        onClick={handleProcess}
                        disabled={processing}
                        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-sm font-medium rounded-lg transition-all shadow-lg shadow-blue-500/20 disabled:opacity-50"
                    >
                        {processing ? (
                            <>
                                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                AI Analysis...
                            </>
                        ) : (
                            <>
                                <span>✨ Process with AI</span>
                            </>
                        )}
                    </button>
                ) : (
                    <div className="flex items-center gap-1 text-xs text-emerald-400 font-medium opacity-75">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Processed
                    </div>
                )}
            </div>
        </div>
    );
}
