const CONTACT_EMAIL = "contact@giosmart-services.fr";
const JSON_HEADERS = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });
}

function clean(value, maxLength) {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

export default {
  async fetch(request) {
    if (request.method === "GET") {
      const ready = Boolean(process.env.RESEND_API_KEY);
      return json(
        { status: ready ? "ready" : "configuration_required" },
        ready ? 200 : 503
      );
    }

    if (request.method !== "POST") {
      return json({ error: "Méthode non autorisée." }, 405);
    }

    const requestUrl = new URL(request.url);
    const origin = request.headers.get("origin");
    if (origin && origin !== requestUrl.origin) {
      return json({ error: "Origine non autorisée." }, 403);
    }

    const contentLength = Number(request.headers.get("content-length") || 0);
    if (contentLength > 20000) {
      return json({ error: "Message trop volumineux." }, 413);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: "Données invalides." }, 400);
    }

    // Invisible field: bots commonly fill it, real visitors never do.
    if (clean(body.website, 200)) {
      return json({ success: true });
    }

    const form = {
      firstName: clean(body.fname, 80),
      lastName: clean(body.lname, 80),
      email: clean(body.email, 254).toLowerCase(),
      phone: clean(body.phone, 40),
      city: clean(body.city, 120),
      service: clean(body.serviceType, 120),
      preferredDate: clean(body.preferredDate, 20),
      message: clean(body.message, 4000),
    };

    const emailIsValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email);
    if (
      !form.firstName || !form.lastName || !emailIsValid || !form.phone ||
      !form.city || !form.service || !form.message
    ) {
      return json({ error: "Merci de vérifier les champs obligatoires." }, 400);
    }

    const apiKey = process.env.RESEND_API_KEY;
    if (!apiKey) {
      return json({ error: "Le service e-mail est temporairement indisponible." }, 503);
    }

    const safe = Object.fromEntries(
      Object.entries(form).map(([key, value]) => [key, escapeHtml(value)])
    );
    const subject = `Demande de devis — ${form.service} — ${form.firstName} ${form.lastName}`;
    const text = [
      `Nouvelle demande depuis giosmart-services.fr`,
      `Nom : ${form.firstName} ${form.lastName}`,
      `E-mail : ${form.email}`,
      `Téléphone : ${form.phone}`,
      `Ville : ${form.city}`,
      `Service : ${form.service}`,
      form.preferredDate ? `Date souhaitée : ${form.preferredDate}` : "",
      "",
      "Message :",
      form.message,
    ].filter(Boolean).join("\n");

    const resendResponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: `Gio Smart <${CONTACT_EMAIL}>`,
        to: [CONTACT_EMAIL],
        reply_to: form.email,
        subject,
        text,
        html: `
          <div style="font-family:Arial,sans-serif;max-width:640px;margin:auto;color:#2c2c2c">
            <h1 style="font-size:24px;color:#3797e4">Nouvelle demande de devis</h1>
            <p><strong>Nom :</strong> ${safe.firstName} ${safe.lastName}</p>
            <p><strong>E-mail :</strong> <a href="mailto:${safe.email}">${safe.email}</a></p>
            <p><strong>Téléphone :</strong> ${safe.phone}</p>
            <p><strong>Ville :</strong> ${safe.city}</p>
            <p><strong>Service :</strong> ${safe.service}</p>
            ${safe.preferredDate ? `<p><strong>Date souhaitée :</strong> ${safe.preferredDate}</p>` : ""}
            <hr style="border:0;border-top:1px solid #eee;margin:24px 0">
            <p><strong>Message :</strong></p>
            <p style="white-space:pre-wrap">${safe.message}</p>
          </div>
        `,
        tags: [{ name: "source", value: "contact_form" }],
      }),
    });

    if (!resendResponse.ok) {
      console.error("Resend contact error:", resendResponse.status);
      return json({ error: "L’envoi a échoué. Utilisez WhatsApp ou réessayez plus tard." }, 502);
    }

    return json({ success: true });
  },
};
