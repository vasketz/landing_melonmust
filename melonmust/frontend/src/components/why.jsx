export default function Why() {
  return (
    <section className="bg-black text-white py-28 px-6 md:px-16 text-center">

      <h2 className="text-3xl font-bold mb-12">
        Why Businesses Choose <span className="text-yellow-400">MelonMust</span>
      </h2>

      <div className="grid md:grid-cols-4 gap-6">

        <div className="bg-white/5 p-6 rounded-xl border border-white/10 hover:bg-white/10 transition">
          <h3 className="text-yellow-400 font-semibold mb-2">Fast Approval</h3>
          <p className="text-gray-400 text-sm">
            Funding decisions within hours.
          </p>
        </div>

        <div className="bg-white/5 p-6 rounded-xl border border-white/10 hover:bg-white/10 transition">
          <h3 className="text-yellow-400 font-semibold mb-2">Flexible Repayment</h3>
          <p className="text-gray-400 text-sm">
            Daily, weekly or monthly options.
          </p>
        </div>

        <div className="bg-white/5 p-6 rounded-xl border border-white/10 hover:bg-white/10 transition">
          <h3 className="text-yellow-400 font-semibold mb-2">Grow Capital</h3>
          <p className="text-gray-400 text-sm">
            Access funding from $10K to $5M.
          </p>
        </div>

        <div className="bg-white/5 p-6 rounded-xl border border-white/10 hover:bg-white/10 transition">
          <h3 className="text-yellow-400 font-semibold mb-2">Simple & Secure</h3>
          <p className="text-gray-400 text-sm">
            No collateral required.
          </p>
        </div>

      </div>

    </section>
  );
}