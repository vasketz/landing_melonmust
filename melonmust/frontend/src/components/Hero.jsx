import { useState } from "react";

export default function Hero() {

  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    amount: "",
    business: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  console.log("API URL:", import.meta.env.VITE_API_URL);
  console.log("FORM DATA:", form);

  const API = import.meta.env.VITE_API_URL;

  try {
    const res = await fetch(`${API}/lead`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    console.log("DATA:", data);

    alert("Application submitted successfully");

  } catch (error) {
    console.error("ERROR:", error);
    alert("Error sending data");
  }
};

const formData = new FormData();

Object.keys(form).forEach(key => {
  formData.append(key, form[key]);
});

  return (
    <section className="relative w-full min-h-screen text-white overflow-hidden pt-32">

      {/* Background */}
      <div className="absolute inset-0">
        <img
          src="/background.png"
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/70"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 w-full px-6 md:px-16 py-20 grid md:grid-cols-2 gap-10 items-center">

        {/* LEFT */}
        <div>
          <h1 className="text-4xl md:text-5xl font-bold text-yellow-400 mb-6 leading-tight">
            Fast Business Funding in 24–48 Hours
          </h1>

          <p className="text-xl md:text-2xl font-semibold mb-6">
            Get approved for up to $500,000 without impacting your credit score.
          </p>

          <ul className="space-y-3 text-gray-300 mb-10">
            <li>✔ No impact on credit score </li>
            <li>✔ Approval in hours, not days  </li>
            <li>✔ 100% secure & confidential</li>
          </ul>

          <div>
            <p className="mb-4 text-lg">
              How much funding do you need?
            </p>

            <div className="flex flex-wrap gap-3">
              {["10000", "100000", "1000000", "5000000"].map((amount) => (
                <button
                  key={amount}
                  type="button"
                  onClick={() => setForm({ ...form, amount })}
                  className="border border-white px-4 py-2 rounded hover:bg-white hover:text-black transition"
                >
                  ${Number(amount).toLocaleString()}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* RIGHT (FORM) */}
        <div className="bg-white/10 backdrop-blur-xl p-8 rounded-2xl border border-white/20 shadow-2xl">

          <h2 className="text-xl font-semibold mb-4 text-center">
            Check Your Funding Eligibility
          </h2>

          <form className="space-y-4" onSubmit={handleSubmit}>

            <div className="grid grid-cols-2 gap-3">
              <input
                name="firstName"
                placeholder="First Name"
                onChange={handleChange}
                className="p-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-yellow-500"
                required
              />
              <input
                name="lastName"
                placeholder="Last Name"
                onChange={handleChange}
                className="p-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-yellow-500"
                required
              />
            </div>

            <input
              name="business"
              placeholder="Business Name"
              onChange={handleChange}
              className="w-full p-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-yellow-500"
            />

            <input
              name="email"
              type="email"
              placeholder="Email"
              onChange={handleChange}
              className="w-full p-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-yellow-500"
              required
            />

            <input
              name="phone"
              placeholder="Phone Number"
              onChange={handleChange}
              className="w-full p-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-yellow-500"
              required
            />

            <input
              name="amount"
              placeholder="Funding Amount"
              value={form.amount}
              onChange={handleChange}
              className="w-full p-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-yellow-500"
              required
            />
            <div className="text-left">
              <label className="text-sm text-gray-300">
                Upload Bank Statements (Optional)
              </label>

              <input
                type="file"
                accept=".pdf,.jpg,.png"
                onChange={(e) => setForm({
                  ...form,
                  file: e.target.files[0]
                })}
                className="w-full mt-2 p-2 rounded bg-white text-black"
              />

              <p className="text-xs text-gray-400 mt-1">
                Speeds up approval process
              </p>
            </div>

            <button
              type="submit"
              className="w-full bg-yellow-500 text-black p-4 rounded-lg font-bold text-lg hover:bg-yellow-400 transition shadow-lg"
            >
              Check My Approval →
            </button>
            <h3 className="text-xl font-semibold mb-4 text-center">
              Takes less than 60 seconds • No credit impact
            </h3>
          </form>

        </div>
      </div>
    </section>
  );
}