export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-black/50 backdrop-blur-md">
      
      <div className="w-full px-6 md:px-16 flex items-center justify-between h-20">

        {/* LOGO */}
        <div className="flex items-center">
         <img 
            src="/Logo.png" 
            alt="MelonMust"
            className="h-28 md:h-40 object-contain drop-shadow-[0_0_10px_rgba(255,200,0,0.6)]"
        />
        </div>
      </div>

    </nav>
  );
}
