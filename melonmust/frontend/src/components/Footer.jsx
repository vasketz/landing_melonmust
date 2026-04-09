export default function Footer() {
  return (
    <footer className="bg-black text-gray-300 border-t border-white/10 mt-20">
        
      <div className="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row justify-between items-start gap-10">
      
        {/* LEFT */}
        <div className="max-w-md">
          <div className="flex items-center gap-3 mb-4">
            <img src="/logo.png" alt="MelonMust" className="w-14 object-contain" />
            <div>
              <p className="text-yellow-400 font-semibold leading-none">
                MelonMust
              </p>
              <p className="text-sm text-gray-400 leading-none">
                Capital
              </p>
            </div>
          </div>
      
          <p className="text-sm text-gray-400 leading-relaxed">
            Business funding solutions designed to help entrepreneurs grow and scale.
          </p>
        </div>
      
        {/* RIGHT */}
        <div className="text-left md:text-right">
          <h4 className="text-white font-semibold mb-3">
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