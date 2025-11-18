// === CONTACT FORM (Flask + Firebase Integrated + Single Click Protection) ===

// Select elements
const form = document.getElementById("eventForm");
const popup = document.getElementById("popup");
const submitBtn = form.querySelector("button[type='submit']");

// Handle form submission
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Disable submit button immediately
  submitBtn.disabled = true;
  submitBtn.textContent = "Submitting...";

  // Collect form data
  const data = {
    name: document.getElementById("name").value.trim(),
    email: document.getElementById("email").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    eventName: document.getElementById("eventName").value.trim(),
    guests: document.getElementById("guests").value.trim(),
    submittedAt: new Date().toISOString()
  };

  console.log("📨 Sending data to Flask:", data);

  try {
    // ✅ Correct Flask route (previously /submit-contact ❌)
    const res = await fetch("/submit_event", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    const json = await res.json();

    if (json.success) {
      console.log("✅ Booking stored successfully in Firebase/Firestore");
      popup.style.display = "flex"; // show success popup
      form.reset();
    } else {
      alert("❌ Submission failed. Try again later.");
      submitBtn.disabled = false;
      submitBtn.textContent = "Submit";
    }
  } catch (err) {
    console.error("⚠️ Error submitting form:", err);
    alert("⚠️ Connection error. Please try again.");
    submitBtn.disabled = false;
    submitBtn.textContent = "Submit";
  }
});

// Close popup
window.closePopup = function () {
  popup.style.display = "none";
  submitBtn.disabled = false; // Allow next submission
  submitBtn.textContent = "Submit";
};

// Navbar toggle (mobile view)
window.toggleMenu = function () {
  document.querySelector(".nav-links").classList.toggle("show");
};
