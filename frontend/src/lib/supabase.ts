import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Missing Supabase environment variables! Please check your .env file.');
  // We don't throw here to avoid White Screen of Death. 
  // The app will fail later but we can handle it in the UI.
}

export const supabase = createClient(supabaseUrl || '', supabaseAnonKey || '');
