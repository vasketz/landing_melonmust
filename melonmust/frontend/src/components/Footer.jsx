export default function Footer() {
  return (
    <footer className="bg-black text-gray-300 border-t border-white/10 mt-20">

      <div className="max-w-7xl mx-auto px-6 py-10 flex flex-col md:flex-row justify-between items-center md:items-start gap-8">

        {/* LEFT */}
        <div className="max-w-md">
          <div className="flex items-center gap-4 mb-4">
            <img
              src="/logo.png"
              alt="MelonMust"
              className="w-20 object-contain"
            />

            <div>
              <p className="text-yellow-400 font-semibold leading-none text-lg">
                MelonMust
              </p>
              <p className="text-sm text-gray-400 leading-none">
                Capital
              </p>
            </div>
          </div>

          <p className="text-sm text-gray-400 leading-relaxed mt-2">
            Business funding solutions designed to help entrepreneurs grow
            and scale.
          </p>
        </div>

        {/* RIGHT */}
        <div className="text-left md:text-right md:self-center">
          <h4 className="text-white font-semibold mb-2">
            Contact
          </h4>

          <p className="text-sm text-gray-400">
            info@melonmust.com
          </p>

          <p className="text-sm text-gray-400">
            561-372-8457
          </p>
        </div>

      </div>

      {/* DIVIDER */}
      <div className="border-t border-white/10"></div>

      {/* BOTTOM */}
      <div className="text-center py-4 text-sm text-gray-500">
        © 2026 MelonMust Capital. All rights reserved.
      </div>

    </footer>
  );
}