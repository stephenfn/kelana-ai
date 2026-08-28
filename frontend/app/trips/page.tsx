"use client";

import Link from "next/link";
import { startTransition, useEffect, useMemo, useState } from "react";
import { TripCard } from "@/components/TripCard";
import { getTrips } from "@/services/tripService";
import type { Trip } from "@/types/trip";

type SortMode = "latest" | "oldest" | "budget";

export default function TripsPage() {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<SortMode>("latest");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadTrips() {
    setLoading(true); setError("");
    try { const loadedTrips = await getTrips(); startTransition(() => setTrips(loadedTrips)); } catch (err) { setError(err instanceof Error ? err.message : "Unable to load your trips."); } finally { setLoading(false); }
  }
  // The loader updates state from an external API response on mount.
  // eslint-disable-next-line react-hooks/set-state-in-effect
  useEffect(() => { void loadTrips(); }, []);

  const visibleTrips = useMemo(() => trips.filter((trip) => `${trip.destination} ${trip.category}`.toLowerCase().includes(query.toLowerCase())).sort((a, b) => sort === "budget" ? b.budget - a.budget : sort === "oldest" ? a.id - b.id : b.id - a.id), [query, sort, trips]);

  return <main className="min-h-screen bg-[#f7f9f8] text-[#142c3b]"><div className="mx-auto max-w-5xl px-5 sm:px-8"><header className="flex items-center justify-between border-b border-[#d8e4e3] py-5"><Link href="/" className="flex items-center gap-3"><span className="brand-mark">K</span><span className="font-bold text-[#123b50]">KelanaAI</span></Link><Link href="/" className="text-sm font-bold text-[#168b82]">+ New trip</Link></header><section className="py-12 sm:py-16"><p className="eyebrow">Your travel archive</p><div className="mt-3 flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><h1 className="text-5xl font-black tracking-[-0.05em] text-[#102c3e]">Trip history</h1><p className="mt-3 text-[#587077]">Every route you have shaped with KelanaAI.</p></div><span className="rounded-full bg-[#e2f3ee] px-4 py-2 text-sm font-bold text-[#17786f]">{trips.length} saved {trips.length === 1 ? "itinerary" : "itineraries"}</span></div><div className="mt-10 flex flex-col gap-3 sm:flex-row"><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search destination or travel style..." className="search-input flex-1" aria-label="Search trips" /><select value={sort} onChange={(event) => setSort(event.target.value as SortMode)} className="search-input sm:w-48" aria-label="Sort trips"><option value="latest">Latest first</option><option value="oldest">Oldest first</option><option value="budget">Highest budget</option></select></div>{loading && <div className="empty-state mt-6"><div className="spinner" /><strong>Loading your journeys...</strong></div>}{error && <div className="result-message mt-6 border border-[#f0c7b7] bg-[#fff4ee] text-[#a14b35]"><strong>We hit a small detour.</strong><span>{error}</span><button onClick={() => void loadTrips()} className="font-bold underline">Retry</button></div>}{!loading && !error && visibleTrips.length > 0 && <div className="mt-6 grid gap-4">{visibleTrips.map((trip) => <TripCard key={trip.id} trip={trip} />)}</div>}{!loading && !error && visibleTrips.length === 0 && <div className="empty-state mt-6"><span className="text-5xl text-[#9dd5c8]">✈</span><strong>{trips.length ? "No trips match your search." : "No trips found yet."}</strong><span>{trips.length ? "Try another destination or style." : "Create your first itinerary and start exploring."}</span>{!trips.length && <Link href="/" className="primary-button mt-3 max-w-xs">Generate a trip <span>→</span></Link>}</div>}</section></div></main>;
}
