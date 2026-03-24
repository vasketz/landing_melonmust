export default function Steps() {
  return (
    <section className="relative py-28 text-white">

      {/* Background */}
      <div className="absolute inset-0">
        <img
          src="/Background_Hero.png"
          alt="bg"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black"></div>
      </div>

      <div className="relative z-10 px-6 md:px-16 text-center max-w-6xl mx-auto">

        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          HOW IT WORKS
        </h2>

        <p className="text-gray-300 mb-12">
          Get Business Funding in Three Simple Steps
        </p>

        <div className="grid md:grid-cols-3 gap-8">

          {/* STEP 1 */}
          <div className="bg-white/5 backdrop-blur-xl p-8 rounded-2xl border border-white/10 hover:scale-105 transition duration-300">
            <div className="w-10 h-10 flex items-center justify-center rounded-full bg-yellow-500 text-black font-bold mx-auto mb-4">
                1
            </div>
            <h3 className="font-semibold mb-2">Apply Online</h3>
            <p className="text-gray-300 text-sm">
              Funding decisions within hours, not days.
            </p>
          </div>

          {/* STEP 2 */}
          <div className="bg-white/5 backdrop-blur-xl p-8 rounded-2xl border border-white/10 hover:scale-105 transition duration-300">
            <div className="w-10 h-10 flex items-center justify-center rounded-full bg-yellow-500 text-black font-bold mx-auto mb-4">
                2
            </div>
            <h3 className="font-semibold mb-2">Get Approved</h3>
            <p className="text-gray-300 text-sm">
              Our team reviews your business profile quickly.
            </p>
          </div>

          {/* STEP 3 */}
          <div className="bg-white/5 backdrop-blur-xl p-8 rounded-2xl border border-white/10 hover:scale-105 transition duration-300">
            <div className="w-10 h-10 flex items-center justify-center rounded-full bg-yellow-500 text-black font-bold mx-auto mb-4">
                3
            </div>
            <h3 className="font-semibold mb-2">Receive Funding</h3>
            <p className="text-gray-300 text-sm">
              Funds deposited in as little as 24 hours.
            </p>
          </div>

        </div>

      </div>
    </section>
  );
}