import { useState } from "react";

const data = [
  {
    q: "How fast can I receive funding?",
    a: "Most businesses receive funding within 24 hours after approval."
  },
  {
    q: "How much funding can I qualify for?",
    a: "You can qualify from $10,000 up to $5,000,000 depending on your profile."
  },
  {
    q: "Do I need collateral?",
    a: "No collateral is required for most funding options."
  },
  {
    q: "How do repayments work?",
    a: "We offer flexible daily, weekly or monthly repayment options."
  }
];

export default function FAQ() {
  const [open, setOpen] = useState(null);

  return (
    <section className="relative py-20 text-white">

      {/* Background */}
      <div className="absolute inset-0">
        <img src="/Background_Hero.png" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-black/80"></div>
      </div>

      <div className="relative z-10 max-w-3xl mx-auto px-6">

        <h2 className="text-3xl font-bold text-center mb-10">
          Frequently Asked Questions
        </h2>

        <div className="space-y-4">
          {data.map((item, i) => (
            <div
              key={i}
              className="border border-white/20 rounded-lg p-4 bg-white/5"
            >
              <button
                className="w-full flex justify-between items-center text-left"
                onClick={() => setOpen(open === i ? null : i)}
              >
                <span>{item.q}</span>
                <span>{open === i ? "-" : "+"}</span>
              </button>

              {open === i && (
                <p className="mt-3 text-gray-300 text-sm">
                  {item.a}
                </p>
              )}
            </div>
          ))}
        </div>

      </div>
    </section>
  );
}