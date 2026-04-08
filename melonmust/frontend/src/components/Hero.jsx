import { useState } from "react";

export default function Hero() {

  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    amount: "",
    business: "",
    file: null,
    website: ""
  });

  const [loading, setLoading] = useState(false);

  // =========================
  // HANDLE CHANGE
  // =========================
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  // =========================
  // SANITIZE INPUT
  // =========================
  const sanitize = (str) => {
    if (!str) return "";
    return str.replace(/[<>]/g, "").trim();
  };

  // =========================
  // VALIDATION
  // =========================
  const validateForm = () => {

    if (!form.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
      return "Invalid email";
    }

    if (form.phone.length < 8) {
      return "Invalid phone number";
    }

    const amount = Number(form.amount);
    if (isNaN(amount) || amount <= 0) {
      return "Invalid amount";
    }

    if (form.file) {
      const allowedTypes = ["application/pdf", "image/png", "image/jpeg"];

      if (!allowedTypes.includes(form.file.type)) {
        return "Invalid file type";
      }

      if (form.file.size > 5 * 1024 * 1024) {
        return "File too large (max 5MB)";
      }
    }

    return null;
  };

  // =========================
  // SUBMIT
  // =========================
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (loading) return; // 🛡️ evita múltiples envíos
    if (form.website) return; // 🛡️ honeypot

    const error = validateForm();
    if (error) {
      alert(error);
      return;
    }

    const API = import.meta.env.VITE_API_URL;

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("firstName", sanitize(form.firstName));
      formData.append("lastName", sanitize(form.lastName));
      formData.append("email", form.email);
      formData.append("phone", form.phone);
      formData.append("amount", form.amount);
      formData.append("business", sanitize(form.business));

      // ✅ usar archivo desde estado (correcto)
      if (form.file) {
        const cleanFile = new File(
          [form.file],
          form.file.name.replace(/[^a-zA-Z0-9.]/g, "_"),
          { type: form.file.type }
        );

        formData.append("file", cleanFile);
      }

      // ⏱️ timeout protección
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);

      const res = await fetch(`${API}/lead`, {
        method: "POST",
        body: formData,
        signal: controller.signal
      });

      clearTimeout(timeout);

      let data = {};
      try {
        data = await res.json();
      } catch {
        data = {};
      }

      if (!res.ok || data.status !== "success") {
        alert(data.detail || "Error submitting application");
        return;
      }

      alert("Application submitted successfully");

      setForm({
        firstName: "",
        lastName: "",
        email: "",
        phone: "",
        amount: "",
        business: "",
        file: null,
        website: ""
      });

    } catch (error) {
      console.error("ERROR:", error);

      if (error.name === "AbortError") {
        alert("Request timeout. Try again.");
      } else {
        alert("Network error. Try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="relative w-full min-h-screen text-white overflow-hidden pt-32">

      <div className="absolute inset-0">
        <img
          src="/background.png"
          alt="Background"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/70"></div>
      </div>

      <div className="relative z-10 w-full px-6 md:px-16 py-20 grid md:grid-cols-2 gap-10 items-center">

        <div>
          <h1 className="text-4xl md:text-5xl font-bold text-yellow-400 mb-6 leading-tight">
            Fast Business Funding in 24–48 Hours
          </h1>

          <p className="text-xl md:text-2xl font-semibold mb-6">
            Get approved for up to $500,000 without impacting your credit score.
          </p>

          <ul className="space-y-3 text-gray-300 mb-10">
            <li>✔ No impact on credit score</li>
            <li>✔ Approval in hours, not days</li>
            <li>✔ 100% secure & confidential</li>
          </ul>
        </div>

        <div className="bg-white/10 backdrop-blur-xl p-8 rounded-2xl border border-white/20 shadow-2xl">

          <h2 className="text-xl font-semibold mb-4 text-center">
            Check Your Funding Eligibility
          </h2>

          <form className="space-y-4" onSubmit={handleSubmit}>

            <input
              type="text"
              name="website"
              value={form.website}
              onChange={handleChange}
              style={{ display: "none" }}
            />

            <div className="grid grid-cols-2 gap-3">
              <input name="firstName" value={form.firstName} placeholder="First Name" onChange={handleChange} className="p-3 rounded-lg text-black" required />
              <input name="lastName" value={form.lastName} placeholder="Last Name" onChange={handleChange} className="p-3 rounded-lg text-black" required />
            </div>

            <input name="business" value={form.business} placeholder="Business Name" onChange={handleChange} className="w-full p-3 rounded-lg text-black" />

            <input name="email" value={form.email} type="email" placeholder="Email" onChange={handleChange} className="w-full p-3 rounded-lg text-black" required />

            <input name="phone" value={form.phone} placeholder="Phone Number" onChange={handleChange} className="w-full p-3 rounded-lg text-black" required />

            <input name="amount" value={form.amount} placeholder="Funding Amount" onChange={handleChange} className="w-full p-3 rounded-lg text-black" required />

            <div className="text-left">
              <label className="text-sm text-gray-300 block mb-2">
                Upload Bank Statements (Optional)
              </label>

              <input
                type="file"
                accept=".pdf,.jpg,.png"
                onChange={(e) =>
                  setForm({
                    ...form,
                    file: e.target.files[0],
                  })
                }
                className="w-full p-2 bg-white text-black rounded"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-yellow-500 text-black p-4 rounded-lg font-bold text-lg hover:bg-yellow-400 transition shadow-lg disabled:opacity-50"
            >
              {loading ? "Sending..." : "Check My Approval →"}
            </button>

            <p className="text-center text-sm text-gray-300">
              🔒 Your data is securely processed. We do not share your information.
            </p>

          </form>

        </div>
      </div>
    </section>
  );
}