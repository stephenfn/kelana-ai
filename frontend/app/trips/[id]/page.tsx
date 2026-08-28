import Link from "next/link";
import { notFound } from "next/navigation";
import { getTrip } from "@/services/tripService";

function makeItinerary(destination: string, days: number) {
  const plans = [`Explore ${destination} with a city walk, local food stops, and a culturally rich landmark.`, "Visit the best neighborhoods and hidden gems, with time for shopping and a relaxed coffee break.", "Enjoy a local experience like a market visit, scenic viewpoint, or iconic attraction.", "Take a day trip or a slow cultural experience to understand the local rhythm.", "Finish with a memorable evening and a relaxed dinner in a lively area."];
  return plans.slice(0, Math.max(1, Math.min(days, plans.length)));
}

export default async function TripDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const tripId = Number(id);
  if (!Number.isInteger(tripId)) notFound();
  let trip;
  try { trip = await getTrip(tripId); } catch { notFound(); }
  const itinerary = makeItinerary(trip.destination, trip.days);
  return <main className="min-h-screen bg-[#f7f9f8] text-[#142c3b]"><div className="mx-auto max-w-5xl px-5 sm:px-8"><header className="flex items-center justify-between border-b border-[#d8e4e3] py-5"><Link href="/" className="flex items-center gap-3"><span className="brand-mark">K</span><span className="font-bold text-[#123b50]">KelanaAI</span></Link><Link href="/trips" className="text-sm font-bold text-[#168b82]">All trips</Link></header><section className="py-12 sm:py-16"><Link href="/trips" className="text-sm font-bold text-[#168b82]">← Back to trips</Link><p className="eyebrow mt-10">Saved itinerary</p><h1 className="mt-3 text-5xl font-black tracking-tighter text-[#102c3e]">{trip.destination}</h1><div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4"><div className="stat"><span>Budget</span><strong>USD {trip.budget.toLocaleString()}</strong></div><div className="stat"><span>Duration</span><strong>{trip.days} days</strong></div><div className="stat"><span>Daily budget</span><strong>USD {trip.daily_budget.toLocaleString()}</strong></div><div className="stat"><span>Category</span><strong>{trip.category}</strong></div></div><div className="mt-12 max-w-3xl"><p className="eyebrow">AI recommendation</p><div className="mt-3">{itinerary.map((item, index) => <article key={item} className="itinerary-item"><span className="day-number">{String(index + 1).padStart(2, "0")}</span><p><strong>Day {index + 1}</strong>{item}</p></article>)}</div></div></section></div></main>;
}
