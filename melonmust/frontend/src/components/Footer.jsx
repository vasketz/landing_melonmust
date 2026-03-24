export default function Footer() {
  return (
    <footer className="bg-black text-white py-20 px-6 md:px-16">

      <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-10 items-center">

        {/* LEFT */}
        <div>
          <img 
            src="/footer_logo.png" 
            className="h-40 mb-0 drop-shadow-lg"
          />

          <p className="text-gray-400 text-sm max-w-md">
            Business funding solutions designed to help entrepreneurs grow and scale.
          </p>
        </div>

        {/* RIGHT */}
        <div className="md:text-right">
          <h3 className="text-xl font-semibold mb-4">
            Contact
          </h3>

          <p className="text-gray-300">info@melonmust.com</p>
          <p className="text-gray-300">561-372-8457</p>
        </div>

      </div>

      {/* divider */}
      <div className="border-t border-white/10 mt-10 pt-6 text-center text-gray-500 text-sm">
        © 2026 MelonMust Capital. All rights reserved.
      </div>

    </footer>
  );
}