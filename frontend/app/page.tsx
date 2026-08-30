"use client";

import type { FormEvent } from "react";
import { useMemo, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { generateTrip } from "@/services/tripService";

type TripForm = { destination: string; budget: string; days: string; travel_style: string };
type SavedTrip = { id: number; destination: string; budget: number; days: number; category: string; daily_budget: number };

const initialForm: TripForm = { destination: "Japan", budget: "2000", days: "5", travel_style: "Family" };

function makeItinerary(destination: string, days: number) {
  const plans = [
    `Explore ${destination} with a gentle city walk, local food stops, and a culturally rich landmark.`,
    "Visit the best neighborhoods and hidden gems, with time for shopping and a relaxed coffee break.",
    "Enjoy a local experience like a market visit, scenic viewpoint, or iconic attraction.",
    "Take a day trip or a slow cultural experience to understand the local rhythm.",
    "Finish with a memorable evening and a relaxed dinner in a lively area.",
  ];
  return plans.slice(0, Math.max(1, Math.min(days, plans.length)));
}

export default function Home() {
  const [form, setForm] = useState<TripForm>(initialForm);
  const [trip, setTrip] = useState<SavedTrip | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  // Check authentication on mount
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    }
  }, [router]);

  const itinerary = useMemo(() => (trip ? makeItinerary(trip.destination, trip.days) : []), [trip]);
  const update = (field: keyof TripForm, value: string) =>
    setForm((current) => ({ ...current, [field]: value }));

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!form.destination.trim() || !form.budget || !form.days) {
      setError("Add a destination, budget, and trip length to continue.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const generatedTrip = await generateTrip({
        destination: form.destination,
        budget: Number(form.budget),
        days: Number(form.days),
        travel_style: form.travel_style,
      });
      setTrip(generatedTrip as SavedTrip);
      router.push("/trips");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to generate itinerary. Please try again."
      );
      setTrip(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen overflow-hidden bg-[#f7f9f8] text-[#142c3b]">
      <div className="mx-auto max-w-7xl px-5 sm:px-8 lg:px-10">
        <header className="flex items-center justify-between border-b border-[#d8e4e3] py-5">
          <a href="#top" className="flex items-center gap-3" aria-label="KelanaAI home"><span className="brand-mark">K</span><span className="font-bold tracking-tight text-[#123b50]">KelanaAI</span></a>
          <span className="hidden text-xs font-bold uppercase tracking-[0.2em] text-[#5f7a7e] sm:block">AI travel studio</span>
        </header>

        <section id="top" className="hero-grid py-10 sm:py-16 lg:py-20">
          <div className="relative z-10 self-center">
            <p className="eyebrow">Your next chapter starts here</p>
            <h1 className="mt-4 max-w-2xl text-5xl font-black leading-[0.95] tracking-[-0.06em] text-[#102c3e] sm:text-7xl lg:text-8xl">Go somewhere<br /><span className="text-[#168b82]">worth remembering.</span></h1>
            <p className="mt-6 max-w-lg text-base leading-7 text-[#587077] sm:text-lg">Tell KelanaAI what kind of trip you want. We will shape the first draft of your adventure.</p>
            <div className="mt-8 flex flex-wrap gap-3 text-sm font-semibold text-[#315d65]"><span className="soft-pill">✦ Personalised routes</span><span className="soft-pill">↗ Built for curious people</span></div>
          </div>
          <div className="hero-image" role="img" aria-label="Aerial view of a tropical coastline"><div className="hero-image-label"><span className="text-xs font-bold uppercase tracking-[0.18em] text-white/70">Featured escape</span><strong>Find your faraway.</strong></div></div>
        </section>

        <section className="grid gap-6 pb-16 lg:grid-cols-[minmax(0,0.82fr)_minmax(0,1.18fr)] lg:gap-10">
          <div className="rounded-4xl bg-[#123b50] p-6 text-white shadow-[0_24px_60px_rgba(18,59,80,0.16)] sm:p-8">
            <div className="mb-8 flex items-start justify-between gap-4"><div><p className="eyebrow text-[#89d1c1]">Build your itinerary</p><h2 className="mt-2 text-3xl font-bold tracking-tight">What are you in the mood for?</h2></div><span className="rounded-full bg-white/10 px-3 py-1 text-xs font-bold text-[#b8eee1]">01 / 01</span></div>
            <form onSubmit={handleSubmit} className="space-y-5">
              <label className="field-label">Destination<input value={form.destination} onChange={(event) => update("destination", event.target.value)} placeholder="e.g. Japan" required /></label>
              <div className="grid gap-5 sm:grid-cols-2"><label className="field-label">Budget <span className="font-normal normal-case tracking-normal text-white/50">USD</span><input type="number" min="1" value={form.budget} onChange={(event) => update("budget", event.target.value)} required /></label><label className="field-label">Days<input type="number" min="1" max="30" value={form.days} onChange={(event) => update("days", event.target.value)} required /></label></div>
              <label className="field-label">Travel style<input value={form.travel_style} onChange={(event) => update("travel_style", event.target.value)} placeholder="e.g. Slow, food-first, outdoors" /></label>
              <button type="submit" disabled={loading} className="primary-button"><span>{loading ? "Sketching your route..." : "Generate my trip"}</span><span aria-hidden="true">→</span></button>
            </form>
            <p className="mt-5 text-xs leading-5 text-white/50">Your preferences become the starting point for a trip that feels like yours.</p>
          </div>

          <div className="min-h-105 rounded-4xl border border-[#d8e4e3] bg-white p-6 shadow-[0_16px_45px_rgba(41,73,77,0.06)] sm:p-8">
            <div className="flex items-center justify-between border-b border-[#e5eeec] pb-5"><div><p className="eyebrow">Your trip preview</p><h2 className="mt-2 text-3xl font-bold tracking-tight text-[#163849]">{trip ? trip.destination : form.destination || "Your destination"}</h2></div><span className="text-3xl" aria-hidden="true">✺</span></div>
            {loading && <div className="result-message bg-[#e2f3ee] text-[#17786f]" role="status"><div className="spinner" /><strong>Making room for wonder...</strong><span>KelanaAI is sketching a route around your preferences.</span></div>}
            {error && <div className="result-message border border-[#f0c7b7] bg-[#fff4ee] text-[#a14b35]" role="alert"><strong>We hit a small detour.</strong><span>{error}</span><button type="button" onClick={() => setError("")} className="mt-2 font-bold underline">Try again</button></div>}
            {!loading && !error && trip && itinerary.length > 0 && <div className="mt-6 space-y-3"><div className="mb-5 grid grid-cols-2 gap-3 sm:grid-cols-3"><div className="stat"><span>Duration</span><strong>{trip.days} days</strong></div><div className="stat"><span>Daily budget</span><strong>${trip.daily_budget.toLocaleString()}</strong></div><div className="stat col-span-2 sm:col-span-1"><span>Travel mood</span><strong>{trip.category}</strong></div></div><p className="eyebrow">A first look</p>{itinerary.map((item, index) => <article key={item} className="itinerary-item"><span className="day-number">{String(index + 1).padStart(2, "0")}</span><p><strong>Day {index + 1}</strong>{item}</p></article>)}</div>}
            {!loading && !error && itinerary.length === 0 && <div className="empty-state"><span className="text-5xl text-[#9dd5c8]">✦</span><strong>Your itinerary will appear here.</strong><span>Choose your destination and let&apos;s make a plan.</span></div>}
          </div>
        </section>
      </div>
      <footer className="border-t border-[#d8e4e3] bg-[#eef5f2]"><div className="mx-auto flex max-w-7xl flex-col gap-4 px-5 py-7 text-sm text-[#587077] sm:flex-row sm:items-center sm:justify-between sm:px-8 lg:px-10"><p>© 2025 KelanaAI. Plan boldly, travel lightly.</p><nav className="flex gap-5 font-semibold text-[#315d65]" aria-label="Footer navigation"><a href="#top" className="hover:text-[#168b82]">Back to top</a><a href="mailto:hello@kelana.ai" className="hover:text-[#168b82]">Contact</a></nav></div></footer>
    </main>
  );
}
