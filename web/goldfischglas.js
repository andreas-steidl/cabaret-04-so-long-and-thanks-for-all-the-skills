/* Das Goldfischglas der vierten Spielzeit.
   Ein Goldfisch schwimmt Runden. Jedes Mal, wenn er vorne vorbeikommt, steigt
   eine Blase mit einer Nummer auf, erreicht die Oberflaeche und zerplatzt.
   Wer sie anklickt (oder Tab und Eingabe), schreibt sie auf den Papierstreifen.
   Der Streifen bleibt (localStorage), der Fisch vergisst.
   Daten und Texte (GOLDFISCHGLAS) kommen aus der Seite. Keine Bibliotheken. */
(function () {
  "use strict";
  const DATEN = window.GOLDFISCHGLAS;
  const glas = document.getElementById("glas");
  const liste = document.getElementById("streifen-liste");
  const leeren = document.getElementById("streifen-leeren");
  const ansage = document.getElementById("glas-ansage");
  const buehne = document.getElementById("glasbuehne");
  if (!DATEN || !glas || !liste) return;

  const NS = "http://www.w3.org/2000/svg";
  const T = DATEN.texte;
  const NUMMERN = DATEN.nummern;
  const SPEICHER = "machsgut-streifen";
  const nachId = {};
  NUMMERN.forEach(function (n) { nachId[n.id] = n; });

  /* Masse des Glases (viewBox 0 0 400 470) */
  const MX = 200, MY = 275, RAND = 150, INNEN = 146;
  const OBERFLAECHE = 188;
  const BAHN_X = 82, BAHN_Y = 338;
  const R_BLASE = 42;
  const RUNDE = 13;                       /* Sekunden je Runde */
  const OMEGA = 2 * Math.PI / RUNDE;

  const medien = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  let ruhig = !!(medien && medien.matches);

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (z) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[z]; });
  }
  function sagen(text) {
    if (!ansage) return;
    ansage.textContent = "";
    window.setTimeout(function () { ansage.textContent = text; }, 40);
  }

  /* ---------- Das Glas zeichnen ---------- */
  function wasserForm() {
    /* der Kreis innen, unterhalb der Wasserlinie: ueber dem Wasser ist Luft */
    const halb = Math.sqrt(INNEN * INNEN - Math.pow(MY - OBERFLAECHE, 2));
    return "M " + (MX - halb).toFixed(2) + " " + OBERFLAECHE + " A " + INNEN + " " + INNEN + " 0 1 0 " + (MX + halb).toFixed(2) + " " + OBERFLAECHE + " Z";
  }
  glas.innerHTML =
    '<svg id="goldfischglas" viewBox="0 0 400 470" role="group" aria-label="' + esc(T.glas) + '">' +
    '<defs>' +
      '<linearGradient id="gg-kegel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0964a" stop-opacity=".62"/><stop offset=".55" stop-color="#f0964a" stop-opacity=".2"/><stop offset="1" stop-color="#f0964a" stop-opacity="0"/></linearGradient>' +
      '<filter id="gg-weich" x="-30%" y="-10%" width="160%" height="120%"><feGaussianBlur stdDeviation="7"/></filter>' +
      '<filter id="gg-hauch" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>' +
      '<radialGradient id="gg-glas" cx=".36" cy=".32" r=".75"><stop offset="0" stop-color="#eeeaf4" stop-opacity=".1"/><stop offset=".72" stop-color="#eeeaf4" stop-opacity=".03"/><stop offset="1" stop-color="#eeeaf4" stop-opacity=".16"/></radialGradient>' +
      '<linearGradient id="gg-wasser" gradientUnits="userSpaceOnUse" x1="0" y1="188" x2="0" y2="425"><stop offset="0" stop-color="#6a3a52"/><stop offset=".3" stop-color="#3b2049"/><stop offset="1" stop-color="#1b0e2b"/></linearGradient>' +
      '<radialGradient id="gg-schein" cx=".5" cy=".1" r=".7"><stop offset="0" stop-color="#f0964a" stop-opacity=".42"/><stop offset="1" stop-color="#f0964a" stop-opacity="0"/></radialGradient>' +
      '<radialGradient id="gg-leib" cx=".68" cy=".34" r=".8"><stop offset="0" stop-color="#ffd59a"/><stop offset=".42" stop-color="#f0964a"/><stop offset="1" stop-color="#b0451a"/></radialGradient>' +
      '<linearGradient id="gg-flosse" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#f0964a" stop-opacity=".95"/><stop offset="1" stop-color="#ffb877" stop-opacity=".45"/></linearGradient>' +
      '<radialGradient id="gg-blase" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#1a0f26" stop-opacity=".42"/><stop offset=".7" stop-color="#2a1a3a" stop-opacity=".3"/><stop offset=".9" stop-color="#eeeaf4" stop-opacity=".1"/><stop offset="1" stop-color="#eeeaf4" stop-opacity=".34"/></radialGradient>' +
      '<radialGradient id="gg-tisch" cx=".5" cy=".4" r=".6"><stop offset="0" stop-color="#7a4a3a"/><stop offset=".6" stop-color="#3a2540"/><stop offset="1" stop-color="#221530"/></radialGradient>' +
      '<clipPath id="gg-innen"><path d="' + wasserForm() + '"/></clipPath>' +
    '</defs>' +
    /* Lampe und Lichtkegel */
    '<g aria-hidden="true">' +
      '<polygon points="180,40 220,40 352,430 48,430" fill="url(#gg-kegel)" filter="url(#gg-weich)" opacity=".55"/>' +
      '<line x1="200" y1="0" x2="200" y2="15" stroke="#6a5878" stroke-width="1.5"/>' +
      '<circle cx="200" cy="40" r="22" fill="#f0964a" opacity=".45" filter="url(#gg-hauch)"/>' +
      '<path d="M 166 40 Q 168 17 200 15 Q 232 17 234 40 Z" fill="#3a2a46" stroke="#7a688a" stroke-width="1"/>' +
      '<ellipse cx="200" cy="40" rx="34" ry="3" fill="#2a1d36"/>' +
      '<circle cx="200" cy="42" r="6.5" fill="#ffe2bd"/>' +
    '</g>' +
    /* Tischchen */
    '<g aria-hidden="true">' +
      '<rect x="194" y="432" width="12" height="38" fill="#2a1c36"/>' +
      '<ellipse cx="200" cy="428" rx="128" ry="11" fill="url(#gg-tisch)" stroke="#5c4a6c" stroke-width="1"/>' +
      '<ellipse cx="200" cy="425" rx="72" ry="5" fill="#000" opacity=".38"/>' +
      '<ellipse cx="200" cy="427" rx="40" ry="3" fill="#f0964a" opacity=".22"/>' +
    '</g>' +
    /* Glaskoerper hinten */
    '<path aria-hidden="true" d="M 110 155 A 150 150 0 1 0 290 155 Z" fill="url(#gg-glas)"/>' +
    /* Wasser */
    '<g clip-path="url(#gg-innen)" aria-hidden="true">' +
      '<rect x="40" y="' + OBERFLAECHE + '" width="320" height="260" fill="url(#gg-wasser)"/>' +
      '<ellipse cx="200" cy="205" rx="130" ry="95" fill="url(#gg-schein)"/>' +
      '<polygon points="170,188 196,188 176,420 132,420" fill="#ffd2a0" opacity=".05"/>' +
      '<polygon points="214,188 236,188 280,420 236,420" fill="#ffd2a0" opacity=".04"/>' +
      '<g opacity=".9">' +
        '<ellipse cx="150" cy="414" rx="14" ry="7" fill="#4b3a5c"/><ellipse cx="172" cy="418" rx="10" ry="5" fill="#6b5878"/>' +
        '<ellipse cx="205" cy="419" rx="16" ry="6" fill="#3e2f50"/><ellipse cx="232" cy="415" rx="11" ry="6" fill="#5e4a6e"/>' +
        '<ellipse cx="255" cy="418" rx="13" ry="5" fill="#463656"/><ellipse cx="188" cy="412" rx="7" ry="4" fill="#806a8a"/>' +
      '</g>' +
    '</g>' +
    /* Der Fisch, gezeichnet nach rechts schauend */
    '<g clip-path="url(#gg-innen)" aria-hidden="true"><g id="gg-fisch" transform="translate(200 ' + BAHN_Y + ') scale(-1 1)">' +
      '<g id="gg-schwanz"><path d="M -26 0 C -36 -6 -44 -22 -56 -26 C -51 -12 -50 -5 -45 0 C -50 5 -51 12 -56 26 C -44 22 -36 6 -26 0 Z" fill="url(#gg-flosse)" stroke="#c4581f" stroke-width=".6"/></g>' +
      '<path d="M -4 -15 C 2 -30 14 -32 22 -13 Z" fill="url(#gg-flosse)" stroke="#c4581f" stroke-width=".5"/>' +
      '<path d="M -12 12 C -16 21 -23 24 -27 20 C -22 17 -18 14 -12 12 Z" fill="url(#gg-flosse)"/>' +
      '<path d="M 32 0 C 32 -12 18 -18 2 -17 C -14 -16 -24 -8 -29 0 C -24 8 -14 16 2 17 C 18 18 32 12 32 0 Z" fill="url(#gg-leib)" stroke="#a8461a" stroke-width=".7"/>' +
      '<path d="M 15 -11 Q 10 0 15 11" fill="none" stroke="#b0451a" stroke-width="1" opacity=".7"/>' +
      '<path d="M -8 -9 Q -2 -13 6 -12" fill="none" stroke="#ffe0b0" stroke-width="1.4" opacity=".5" stroke-linecap="round"/>' +
      '<g id="gg-brust"><path d="M 8 5 C 4 13 -2 17 -6 15 C -2 11 2 8 8 5 Z" fill="#ffb877" opacity=".8"/></g>' +
      '<circle cx="22" cy="-4" r="3.6" fill="#fff4e4"/><circle cx="22.8" cy="-4" r="2.1" fill="#24122e"/><circle cx="23.4" cy="-4.8" r=".7" fill="#fff"/>' +
    '</g></g>' +
    /* Blasen */
    '<g id="gg-blasen"></g>' +
    /* Wasserlinie und Glas vorne */
    '<g aria-hidden="true" pointer-events="none">' +
      '<ellipse cx="200" cy="' + OBERFLAECHE + '" rx="117" ry="7" fill="#f0964a" fill-opacity=".14" stroke="#ffd6aa" stroke-opacity=".5" stroke-width="1"/>' +
      '<path d="M 110 155 A 150 150 0 1 0 290 155" fill="none" stroke="#eeeaf4" stroke-opacity=".46" stroke-width="1.6"/>' +
      '<ellipse cx="200" cy="155" rx="90" ry="9" fill="none" stroke="#eeeaf4" stroke-opacity=".58" stroke-width="1.5"/>' +
      '<ellipse cx="200" cy="156.5" rx="86" ry="6.5" fill="none" stroke="#f0964a" stroke-opacity=".25" stroke-width="1"/>' +
      '<path d="M 70.3 227.8 A 138 138 0 0 1 120.8 162" fill="none" stroke="#ffffff" stroke-opacity=".5" stroke-width="5" stroke-linecap="round"/>' +
      '<path d="M 66 262 A 138 138 0 0 1 67.5 246" fill="none" stroke="#ffffff" stroke-opacity=".38" stroke-width="3" stroke-linecap="round"/>' +
      '<path d="M 329.7 322.2 A 138 138 0 0 1 288.7 380.7" fill="none" stroke="#ffd6aa" stroke-opacity=".32" stroke-width="3" stroke-linecap="round"/>' +
      '<ellipse cx="300" cy="250" rx="7" ry="34" fill="#ffffff" opacity=".06" transform="rotate(-12 300 250)"/>' +
      '<ellipse cx="129" cy="204" rx="5" ry="11" fill="#ffffff" opacity=".45" transform="rotate(32 129 204)"/>' +
    '</g>' +
    '</svg>';

  const fisch = document.getElementById("gg-fisch");
  const schwanz = document.getElementById("gg-schwanz");
  const brust = document.getElementById("gg-brust");
  const blasenSchicht = document.getElementById("gg-blasen");

  /* ---------- Der Streifen ---------- */
  function lesen() {
    try {
      const roh = window.localStorage.getItem(SPEICHER);
      const daten = roh ? JSON.parse(roh) : [];
      return Array.isArray(daten) ? daten.filter(function (e) { return e && nachId[e.id] && typeof e.zeit === "string"; }) : [];
    } catch (e) { return []; }
  }
  function schreiben(eintraege) {
    try { window.localStorage.setItem(SPEICHER, JSON.stringify(eintraege)); } catch (e) { /* ohne Speicher bleibt es eine Sitzung lang */ }
  }
  let streifen = lesen();

  function zwei(z) { return (z < 10 ? "0" : "") + z; }
  function uhrzeit(d) { return zwei(d.getHours()) + ":" + zwei(d.getMinutes()); }
  function zeitText(iso) {
    const d = new Date(iso);
    if (isNaN(d.getTime())) return "";
    const heute = new Date();
    const gleicherTag = d.getFullYear() === heute.getFullYear() && d.getMonth() === heute.getMonth() && d.getDate() === heute.getDate();
    return gleicherTag ? uhrzeit(d) : T.datum(d) + " " + uhrzeit(d);
  }

  function zeichnen(frisch) {
    liste.textContent = "";
    if (!streifen.length) {
      const li = document.createElement("li");
      li.className = "leer";
      li.textContent = T.leer;
      liste.appendChild(li);
    }
    streifen.forEach(function (e) {
      const n = nachId[e.id];
      const li = document.createElement("li");
      if (e.id === frisch) li.className = "frisch";
      const a = document.createElement("a");
      a.href = "#" + n.id;
      const nr = document.createElement("span");
      nr.className = "snr";
      nr.textContent = n.extra ? T.extraKurz : n.nr;
      a.appendChild(nr);
      a.appendChild(document.createTextNode(" " + n.name));
      const zeit = document.createElement("time");
      zeit.dateTime = e.zeit;
      zeit.textContent = zeitText(e.zeit);
      const d = new Date(e.zeit);
      if (!isNaN(d.getTime())) zeit.title = d.toLocaleString(DATEN.sprache);
      li.appendChild(a);
      li.appendChild(zeit);
      liste.appendChild(li);
    });
    if (leeren) leeren.disabled = !streifen.length;
  }
  zeichnen(null);

  function aufschreiben(n) {
    if (streifen.some(function (e) { return e.id === n.id; })) {
      zeichnen(n.id);
      sagen(T.schonDa(n));
      return;
    }
    const jetzt = new Date();             /* aus der Uhr gelesen, nicht geschaetzt */
    streifen.push({ id: n.id, zeit: jetzt.toISOString() });
    schreiben(streifen);
    zeichnen(n.id);
    sagen(T.geschrieben(n, uhrzeit(jetzt)));
  }

  if (leeren) {
    leeren.addEventListener("click", function () {
      streifen = [];
      schreiben(streifen);
      zeichnen(null);
      sagen(T.geleert);
    });
  }
  window.addEventListener("storage", function (e) {
    if (e.key === SPEICHER) { streifen = lesen(); zeichnen(null); }
  });

  /* ---------- Blasen ---------- */
  function zeilen(name) {
    if (name.length <= 11) return [name];
    let beste = null;
    for (let i = 1; i < name.length - 1; i++) {
      if (name[i] !== "-") continue;
      const a = name.slice(0, i + 1), b = name.slice(i + 1);
      const wert = Math.max(a.length, b.length);
      if (!beste || wert < beste.wert) beste = { wert: wert, teile: [a, b] };
    }
    return beste ? beste.teile : [name];
  }

  const blasen = [];
  let naechste = 0;

  function knoten(name, merkmale, eltern) {
    const e = document.createElementNS(NS, name);
    for (const k in merkmale) e.setAttribute(k, merkmale[k]);
    if (eltern) eltern.appendChild(e);
    return e;
  }

  function blaseMachen(x, y) {
    const n = NUMMERN[naechste];
    naechste = (naechste + 1) % NUMMERN.length;
    const g = knoten("g", { class: "blase", role: "button", tabindex: "0", "aria-label": T.blase(n) }, blasenSchicht);
    knoten("circle", { class: "blase-rund", r: String(R_BLASE), fill: "url(#gg-blase)" }, g);
    knoten("path", { class: "blase-glanz", d: "M -29 -17 A 34 34 0 0 1 -12 -31", fill: "none" }, g);
    knoten("circle", { class: "blase-funke", cx: "22", cy: "-24", r: "2.2" }, g);
    const z = zeilen(n.name);
    const kopf = knoten("text", { class: "blase-nr", x: "0", y: z.length > 1 ? "-15" : "-8", "text-anchor": "middle" }, g);
    kopf.textContent = n.extra ? T.extraKurz.toUpperCase() : T.nrKurz + " " + n.nr;
    z.forEach(function (teil, i) {
      const t = knoten("text", { class: "blase-name", x: "0", y: String((z.length > 1 ? 2 : 9) + i * 14), "text-anchor": "middle" }, g);
      t.textContent = teil;
    });
    const b = { n: n, g: g, x0: x, x: x, y: y, alter: 0, wackel: Math.random() * 6, hover: false, fokus: false, ende: 0, art: "" };
    g.addEventListener("pointerenter", function () { b.hover = true; });
    g.addEventListener("pointerleave", function () { b.hover = false; });
    g.addEventListener("focus", function () { b.fokus = true; });
    g.addEventListener("blur", function () { b.fokus = false; });
    g.addEventListener("click", function () { fangen(b); });
    g.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") { e.preventDefault(); fangen(b); }
    });
    blasen.push(b);
    if (buehne && buehne.contains(document.activeElement)) sagen(T.steigt(n));
    return b;
  }

  function stilllegen(b) {
    b.g.setAttribute("tabindex", "-1");
    b.g.setAttribute("aria-hidden", "true");
    b.g.style.pointerEvents = "none";
  }

  function fangen(b) {
    if (b.art) return;
    const hatteFokus = document.activeElement === b.g;
    b.art = "gefangen";
    b.ende = 0;
    stilllegen(b);
    aufschreiben(b.n);
    if (hatteFokus) glas.focus({ preventScroll: true });
    if (ruhig) entfernen(b);
  }

  function platzen(b) {
    b.art = "platzt";
    b.ende = 0;
    stilllegen(b);
    if (ruhig) { entfernen(b); return; }
    for (let i = 0; i < 7; i++) {
      const w = i / 7 * 2 * Math.PI + Math.random() * .4;
      knoten("circle", { class: "tropfen", cx: "0", cy: "0", r: "1.8", "data-w": String(w) }, b.g);
    }
  }

  function entfernen(b) {
    const i = blasen.indexOf(b);
    if (i >= 0) blasen.splice(i, 1);
    if (b.g.parentNode) b.g.parentNode.removeChild(b.g);
  }

  function aktiveBlase() {
    for (let i = 0; i < blasen.length; i++) if (!blasen[i].art) return blasen[i];
    return null;
  }

  /* ---------- Bewegung ---------- */
  const z = {
    theta: Math.PI / 2 - OMEGA * 2.2,     /* in gut zwei Sekunden vorne */
    r: 1, rZiel: 1,
    zeit: 0, schwanz: 0,
    wende: 22 + Math.random() * 20,
    letzteBlase: -99,
    runde: null,
    ruhePause: .6
  };

  function fischSetzen(x, y, sx, s, hell, schlag, flattern) {
    fisch.setAttribute("transform", "translate(" + x.toFixed(2) + " " + y.toFixed(2) + ") scale(" + (sx * s).toFixed(3) + " " + s.toFixed(3) + ")");
    fisch.setAttribute("opacity", hell.toFixed(3));
    schwanz.setAttribute("transform", "rotate(" + schlag.toFixed(2) + " -26 0)");
    brust.setAttribute("transform", "translate(8 5) scale(1 " + flattern.toFixed(3) + ") translate(-8 -5)");
  }

  function ruhePose() {
    fischSetzen(MX, BAHN_Y + 6, -1, 1.05, 1, 0, 1);
  }

  function schritt(dt) {
    z.zeit += dt;
    if (ruhig) { schrittRuhig(dt); return; }

    /* gelegentliche Wende */
    if (z.zeit >= z.wende) { z.rZiel = -z.rZiel; z.wende = z.zeit + 20 + Math.random() * 26; }
    const d = z.rZiel - z.r;
    z.r += Math.sign(d) * Math.min(Math.abs(d), dt * .75);

    z.theta += OMEGA * z.r * dt;
    const tiefe = Math.sin(z.theta);       /* 1 = vorne, -1 = hinten */
    const x = MX + BAHN_X * Math.cos(z.theta);
    const y = BAHN_Y + 20 * tiefe + Math.sin(z.zeit * .9) * 4;
    const s = .9 + .2 * tiefe;
    const blick = -tiefe * z.r;            /* Vorzeichen = Schwimmrichtung */
    const sx = (blick < 0 ? -1 : 1) * Math.max(.14, Math.abs(blick));
    z.schwanz += dt * (3.2 + 2.6 * Math.abs(z.r) + (Math.abs(d) > .01 ? 3 : 0));
    fischSetzen(x, y, sx, s, .74 + .26 * (tiefe + 1) / 2, Math.sin(z.schwanz) * 15, .75 + .25 * Math.sin(z.schwanz * 1.3 + 1));

    /* vorne vorbei? */
    const runde = Math.floor((z.theta - Math.PI / 2) / (2 * Math.PI));
    if (z.runde === null) z.runde = runde;
    if (runde !== z.runde) {
      z.runde = runde;
      if (z.zeit - z.letzteBlase > 6 && !aktiveBlase()) {
        z.letzteBlase = z.zeit;
        const mund = x + sx * s * 32;
        blaseMachen(mund, y - 16);
      }
    }

    for (let i = blasen.length - 1; i >= 0; i--) {
      const b = blasen[i];
      b.wackel += dt;
      if (b.art === "platzt") {
        b.ende += dt;
        const t = Math.min(1, b.ende / .38);
        b.g.setAttribute("transform", "translate(" + b.x.toFixed(2) + " " + b.y.toFixed(2) + ") scale(" + (1 + .35 * t).toFixed(3) + ")");
        b.g.setAttribute("opacity", (1 - t).toFixed(3));
        const tropfen = b.g.querySelectorAll(".tropfen");
        for (let k = 0; k < tropfen.length; k++) {
          const w = parseFloat(tropfen[k].getAttribute("data-w"));
          tropfen[k].setAttribute("cx", (Math.cos(w) * (R_BLASE + 16 * t)).toFixed(2));
          tropfen[k].setAttribute("cy", (Math.sin(w) * (R_BLASE + 16 * t) - 10 * t).toFixed(2));
        }
        if (t >= 1) entfernen(b);
        continue;
      }
      if (b.art === "gefangen") {
        b.ende += dt;
        const t = Math.min(1, b.ende / .4);
        b.g.setAttribute("transform", "translate(" + b.x.toFixed(2) + " " + (b.y + 60 * t * t).toFixed(2) + ") scale(" + (1 - .7 * t).toFixed(3) + ")");
        b.g.setAttribute("opacity", (1 - t).toFixed(3));
        if (t >= 1) entfernen(b);
        continue;
      }
      if (!(b.hover || b.fokus)) {
        b.alter += dt;
        b.y -= (13 + Math.min(b.alter, 3) * 3) * dt;
      }
      const groesse = Math.min(1, .16 + b.alter * .42);
      b.x = b.x0 + Math.sin(b.wackel * 1.6) * 6;
      const r = R_BLASE * groesse;
      const grenze = Math.sqrt(Math.max(0, INNEN * INNEN - Math.pow(b.y - MY, 2))) - r - 4;
      if (b.x0 > MX + grenze) b.x0 = MX + grenze;
      if (b.x0 < MX - grenze) b.x0 = MX - grenze;
      b.g.setAttribute("transform", "translate(" + b.x.toFixed(2) + " " + b.y.toFixed(2) + ") scale(" + groesse.toFixed(3) + ")");
      if (b.y - r * .55 <= OBERFLAECHE) platzen(b);
    }
  }

  function schrittRuhig(dt) {
    const b = aktiveBlase();
    if (!b) {
      z.ruhePause -= dt;
      if (z.ruhePause <= 0) {
        const neu = blaseMachen(MX, 262);
        neu.g.setAttribute("transform", "translate(" + MX + " 262)");
        z.ruhePause = 1.4;
      }
      return;
    }
    if (!(b.hover || b.fokus)) b.alter += dt;
    if (b.alter > 7) entfernen(b);
  }

  /* ---------- Schleife ---------- */
  let sichtbar = true, laeuft = false, vorher = 0;
  function bild(jetzt) {
    if (!sichtbar || document.hidden) { laeuft = false; return; }
    const dt = Math.min(.1, Math.max(0, (jetzt - vorher) / 1000));
    vorher = jetzt;
    schritt(dt);
    window.requestAnimationFrame(bild);
  }
  function starten() {
    if (laeuft || !sichtbar || document.hidden) return;
    laeuft = true;
    vorher = performance.now();
    window.requestAnimationFrame(bild);
  }

  function ruheWechsel() {
    ruhig = !!(medien && medien.matches);
    blasen.slice().forEach(entfernen);
    z.ruhePause = .6;
    z.letzteBlase = -99;
    z.runde = null;
    if (ruhig) ruhePose();
  }
  if (ruhig) ruhePose();
  if (medien) {
    if (medien.addEventListener) medien.addEventListener("change", ruheWechsel);
    else if (medien.addListener) medien.addListener(ruheWechsel);
  }

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (eintraege) {
      sichtbar = eintraege[0].isIntersecting;
      starten();
    }).observe(glas);
  }
  document.addEventListener("visibilitychange", starten);
  starten();
})();

/* Die kleine Uhr im Kopf zeigt die Uhrzeit des Besuchers, gemessen, nicht geschaetzt. */
(function () {
  "use strict";
  const stunde = document.getElementById("uhr-stunde");
  const minute = document.getElementById("uhr-minute");
  if (!stunde || !minute) return;
  function stellen() {
    const d = new Date();
    const m = d.getMinutes() + d.getSeconds() / 60;
    const h = (d.getHours() % 12) + m / 60;
    minute.setAttribute("transform", "rotate(" + (m * 6).toFixed(1) + " 50 50)");
    stunde.setAttribute("transform", "rotate(" + (h * 30).toFixed(1) + " 50 50)");
  }
  stellen();
  window.setInterval(stellen, 15000);
})();
