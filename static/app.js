/**
 * Prāṇa AI (प्राण AI) — Client Application Controller
 * Uncluttered Sidebar Navigation, Reactive Atmospheric Telemetry,
 * Diurnal Thermal Inversion Visualizer & GenAI Smog Resilience Engine.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Global Application State
  const state = {
    city: 'Delhi-NCR',
    persona: 'family_with_kids',
    activeTab: 'tab-overview',
    aqiData: null,
    routineData: null,
    iaqData: null,
    impactData: null,
    theme: localStorage.getItem('prana_theme') || 'dark'
  };

  // DOM Selectors
  const dom = {
    sidebar: document.getElementById('main-sidebar'),
    mobileToggle: document.getElementById('mobile-toggle'),
    themeToggle: document.getElementById('theme-toggle'),
    navItems: document.querySelectorAll('.nav-item'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    globalCitySelect: document.getElementById('global-city-select'),
    globalPersonaSelect: document.getElementById('global-persona-select'),
    emergencyBannerText: document.getElementById('emergency-banner-text'),
    navAqiBadge: document.getElementById('nav-aqi-badge'),
    sidebarStatusTitle: document.getElementById('sidebar-status-title'),
    sidebarSafeWindow: document.getElementById('sidebar-safe-window'),
    latencyBadge: document.getElementById('latency-badge'),

    // Tab 1: Overview
    heroCityCountry: document.getElementById('hero-city-country'),
    heroAqiCategory: document.getElementById('hero-aqi-category'),
    heroAqiValue: document.getElementById('hero-aqi-value'),
    heroDominantPollutant: document.getElementById('hero-dominant-pollutant'),
    gaugeFillCircle: document.getElementById('gauge-fill-circle'),
    heroCigarettesValue: document.getElementById('hero-cigarettes-value'),
    heroSafeVentWindow: document.getElementById('hero-safe-vent-window'),
    heroHealthAdvisory: document.getElementById('hero-health-advisory'),
    inversionTimelineTrack: document.getElementById('inversion-timeline-track'),
    inversionExplanationText: document.getElementById('inversion-explanation-text'),
    valPm25: document.getElementById('val-pm25'),
    valPm10: document.getElementById('val-pm10'),
    valNo2: document.getElementById('val-no2'),
    valCo: document.getElementById('val-co'),
    valO3: document.getElementById('val-o3'),
    valTempHum: document.getElementById('val-temp-hum'),

    // Tab 2: Routine
    btnRefreshRoutine: document.getElementById('btn-refresh-routine'),
    btnPrintRoutine: document.getElementById('btn-print-routine'),
    routinePm25Saved: document.getElementById('routine-pm25-saved'),
    routineCigsAverted: document.getElementById('routine-cigs-averted'),
    routineCo2Cut: document.getElementById('routine-co2-cut'),
    routineSafeSlot: document.getElementById('routine-safe-slot'),
    routineStepsContainer: document.getElementById('routine-steps-container'),

    // Tab 3: IAQ
    iaqForm: document.getElementById('iaq-calculator-form'),
    roomNameInput: document.getElementById('room-name-input'),
    roomLengthInput: document.getElementById('room-length-input'),
    roomWidthInput: document.getElementById('room-width-input'),
    roomHeightInput: document.getElementById('room-height-input'),
    smogRiskSelect: document.getElementById('smog-risk-select'),
    resRoomVolume: document.getElementById('res-room-volume'),
    resTargetCadr: document.getElementById('res-target-cadr'),
    resTargetAch: document.getElementById('res-target-ach'),
    plantsDisplayGrid: document.getElementById('plants-display-grid'),
    hacksDisplayList: document.getElementById('hacks-display-list'),

    // Tab 4: Impact
    commuteKmSlider: document.getElementById('commute-km-slider'),
    commuteKmLabel: document.getElementById('commute-km-label'),
    commuteModeSelect: document.getElementById('commute-mode-select'),
    chkIaqFilter: document.getElementById('chk-iaq-filter'),
    chkVentProtocol: document.getElementById('chk-vent-protocol'),
    meterPm25Shielded: document.getElementById('meter-pm25-shielded'),
    meterCigsShielded: document.getElementById('meter-cigs-shielded'),
    meterCo2Saved: document.getElementById('meter-co2-saved'),
    meterCarKm: document.getElementById('meter-car-km'),
    meterPediatricRisk: document.getElementById('meter-pediatric-risk'),
    impactNarrativeContent: document.getElementById('impact-narrative-content'),
    alternativesTableBody: document.getElementById('alternatives-table-body'),

    // Tab 5: Community
    grievanceForm: document.getElementById('grievance-form'),
    grievanceIssueSelect: document.getElementById('grievance-issue-select'),
    grievanceWardInput: document.getElementById('grievance-ward-input'),
    grievanceLandmarkInput: document.getElementById('grievance-landmark-input'),
    grievanceResidentsInput: document.getElementById('grievance-residents-input'),
    grievancePriorityBadge: document.getElementById('grievance-priority-badge'),
    grievanceLetterText: document.getElementById('grievance-letter-text'),
    grievanceStatutoryBasis: document.getElementById('grievance-statutory-basis'),
    whatsappBroadcastText: document.getElementById('whatsapp-broadcast-text'),

    // Tab 6: Chat
    chatThread: document.getElementById('chat-messages-thread'),
    chatForm: document.getElementById('chat-input-form'),
    chatInput: document.getElementById('chat-message-input'),
    promptChips: document.querySelectorAll('.prompt-chips-wrap .chip')
  };

  // --- Theme Controller ---
  function applyTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('prana_theme', theme);
    if (dom.themeToggle) {
      dom.themeToggle.querySelector('.theme-icon').textContent = theme === 'light' ? '☀️' : '🌙';
    }
  }
  applyTheme(state.theme);

  if (dom.themeToggle) {
    dom.themeToggle.addEventListener('click', () => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme(state.theme);
    });
  }

  // --- Mobile Drawer Toggle ---
  if (dom.mobileToggle && dom.sidebar) {
    dom.mobileToggle.addEventListener('click', () => {
      dom.sidebar.classList.toggle('mobile-open');
    });
  }

  // --- Uncluttered Tab Switcher ---
  dom.navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetTab = item.getAttribute('data-tab');
      switchTab(targetTab);
      if (window.innerWidth <= 768 && dom.sidebar) {
        dom.sidebar.classList.remove('mobile-open');
      }
    });
  });

  function switchTab(tabId) {
    state.activeTab = tabId;
    dom.navItems.forEach(item => {
      const match = item.getAttribute('data-tab') === tabId;
      item.classList.toggle('active', match);
      item.setAttribute('aria-selected', match ? 'true' : 'false');
    });

    dom.tabPanes.forEach(pane => {
      pane.classList.toggle('active', pane.id === tabId);
    });
  }

  // --- Global City & Persona Listeners ---
  if (dom.globalCitySelect) {
    dom.globalCitySelect.addEventListener('change', (e) => {
      state.city = e.target.value;
      refreshAllData();
    });
  }

  if (dom.globalPersonaSelect) {
    dom.globalPersonaSelect.addEventListener('change', (e) => {
      state.persona = e.target.value;
      fetchRoutinePlan();
    });
  }

  // --- API Client with Deterministic Offline Fallbacks ---
  async function apiFetch(endpoint, options = {}) {
    const start = performance.now();
    try {
      const response = await fetch(endpoint, options);
      const elapsed = Math.round(performance.now() - start);
      if (dom.latencyBadge) dom.latencyBadge.textContent = `${elapsed}ms`;
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (err) {
      console.warn(`[PranaAPI] Network or route error on ${endpoint}:`, err);
      return null;
    }
  }

  // --- 1. Fetch AQI Snapshot & Diurnal Inversion Curve ---
  async function fetchAQISnapshot() {
    const data = await apiFetch(`/api/aqi/snapshot?city=${encodeURIComponent(state.city)}`);
    if (!data) return; // Retain existing on error

    state.aqiData = data;

    // Header & Sidebar Telemetry
    if (dom.navAqiBadge) dom.navAqiBadge.textContent = data.aqi;
    if (dom.sidebarStatusTitle) {
      dom.sidebarStatusTitle.textContent = data.thermal_inversion_active ? 'Inversion Active' : 'Boundary Layer Clear';
    }
    if (dom.sidebarSafeWindow) {
      dom.sidebarSafeWindow.textContent = `Vent: ${data.safe_ventilation_window}`;
    }
    if (dom.emergencyBannerText) {
      dom.emergencyBannerText.textContent = `${data.health_headline} • Safe Vent: ${data.safe_ventilation_window}`;
    }

    // Tab 1 Hero Gauge
    if (dom.heroCityCountry) dom.heroCityCountry.textContent = `${data.city_name}, ${data.country}`;
    if (dom.heroAqiCategory) {
      dom.heroAqiCategory.textContent = data.category;
      applyCategoryColor(dom.heroAqiCategory, data.aqi);
    }
    if (dom.heroAqiValue) dom.heroAqiValue.textContent = data.aqi;
    if (dom.heroDominantPollutant) dom.heroDominantPollutant.textContent = `Dominant: ${data.dominant_pollutant}`;
    if (dom.heroCigarettesValue) dom.heroCigarettesValue.textContent = data.cigarette_equivalent;
    if (dom.heroSafeVentWindow) dom.heroSafeVentWindow.textContent = data.safe_ventilation_window;
    if (dom.heroHealthAdvisory) dom.heroHealthAdvisory.textContent = data.vulnerable_warning;

    // Radial SVG Gauge calculation: stroke-dasharray is 515
    if (dom.gaugeFillCircle) {
      const capped = Math.min(500, Math.max(0, data.aqi));
      const offset = 515 - (515 * (capped / 500));
      dom.gaugeFillCircle.style.strokeDashoffset = offset;
      dom.gaugeFillCircle.style.stroke = getAQIColor(data.aqi);
    }

    // Diurnal Inversion Timeline
    renderInversionTimeline(data.inversion_curve);

    // Criteria Pollutant Grid
    const p = data.pollutants;
    if (dom.valPm25) dom.valPm25.innerHTML = `${p.pm25.toFixed(1)} <small>µg/m³</small>`;
    if (dom.valPm10) dom.valPm10.innerHTML = `${p.pm10.toFixed(1)} <small>µg/m³</small>`;
    if (dom.valNo2) dom.valNo2.innerHTML = `${p.no2.toFixed(1)} <small>µg/m³</small>`;
    if (dom.valCo) dom.valCo.innerHTML = `${p.co.toFixed(1)} <small>mg/m³</small>`;
    if (dom.valO3) dom.valO3.innerHTML = `${p.o3.toFixed(1)} <small>µg/m³</small>`;
    if (dom.valTempHum) dom.valTempHum.textContent = `${p.temp_c}°C / ${p.humidity_pct}%`;
  }

  function getAQIColor(aqi) {
    if (aqi <= 50) return '#10b981';
    if (aqi <= 100) return '#06b6d4';
    if (aqi <= 200) return '#f59e0b';
    if (aqi <= 300) return '#f97316';
    return '#ef4444';
  }

  function applyCategoryColor(el, aqi) {
    el.style.backgroundColor = getAQIColor(aqi);
  }

  // --- Render 24-Hour Diurnal Inversion Timeline ---
  function renderInversionTimeline(curve) {
    if (!dom.inversionTimelineTrack || !curve) return;
    dom.inversionTimelineTrack.innerHTML = '';

    curve.forEach(pt => {
      const col = document.createElement('div');
      col.className = 'timeline-bar-col';
      col.title = `${pt.label}: Smog Trap ${pt.smog_trap_index}%, Mixing Height ${pt.mixing_height_m}m (${pt.ventilation_safe ? 'Safe to Ventilate' : 'Sealed Window Window'})`;

      const bar = document.createElement('div');
      bar.className = 'timeline-bar';
      if (pt.ventilation_safe) bar.classList.add('safe-window');
      bar.style.height = `${Math.max(12, pt.smog_trap_index)}%`;

      const lbl = document.createElement('span');
      lbl.className = 'timeline-hour-lbl';
      // Label every 3 hours for clean layout
      lbl.textContent = (pt.hour % 3 === 0) ? pt.label.replace(':00', '') : '';

      col.appendChild(bar);
      col.appendChild(lbl);
      dom.inversionTimelineTrack.appendChild(col);
    });
  }

  // --- 2. Fetch Daily Routine Plan ---
  async function fetchRoutinePlan() {
    const data = await apiFetch(`/api/routine/plan?city=${encodeURIComponent(state.city)}&persona=${encodeURIComponent(state.persona)}`, {
      method: 'POST'
    });
    if (!data) return;

    state.routineData = data;

    if (dom.routinePm25Saved) dom.routinePm25Saved.textContent = `${data.total_pm25_saved_ug} µg`;
    if (dom.routineCigsAverted) dom.routineCigsAverted.textContent = data.cigarettes_toxicity_averted;
    if (dom.routineCo2Cut) dom.routineCo2Cut.textContent = `${data.total_co2_cut_kg} kg`;
    if (dom.routineSafeSlot) dom.routineSafeSlot.textContent = data.safe_ventilation_window;

    renderRoutineSteps(data.steps);
  }

  function renderRoutineSteps(steps) {
    if (!dom.routineStepsContainer || !steps) return;
    dom.routineStepsContainer.innerHTML = '';

    steps.forEach((s, idx) => {
      const card = document.createElement('div');
      card.className = 'step-card';

      card.innerHTML = `
        <div class="step-top-row">
          <span class="step-time-badge">⏱️ ${s.time_window}</span>
          <span class="step-risk-badge ${s.risk_level}">${s.risk_level} RISK</span>
        </div>
        <h3 class="step-title">${idx + 1}. ${s.activity_name}</h3>
        <p class="step-recommendation">${s.recommendation}</p>
        <div class="step-rationale">
          <strong>🔬 Science Rationale:</strong> ${s.scientific_rationale}
        </div>
        <div class="step-metrics-row">
          <span>🛡️ PM2.5 Shielded: +${s.pm25_exposure_saved_ug} µg</span>
          ${s.emission_cut_kg_co2 > 0 ? `<span>🌿 Carbon Cut: -${s.emission_cut_kg_co2} kg CO₂</span>` : ''}
        </div>
      `;
      dom.routineStepsContainer.appendChild(card);
    });
  }

  if (dom.btnRefreshRoutine) {
    dom.btnRefreshRoutine.addEventListener('click', () => {
      fetchRoutinePlan();
    });
  }

  if (dom.btnPrintRoutine) {
    dom.btnPrintRoutine.addEventListener('click', () => {
      window.print();
    });
  }

  // --- 3. Indoor IAQ Sizing & Corsi-Rosenthal Calculation ---
  async function submitIAQCalculation(e) {
    if (e) e.preventDefault();

    const payload = {
      room_name: dom.roomNameInput ? dom.roomNameInput.value : 'Living Space',
      length_ft: parseFloat(dom.roomLengthInput ? dom.roomLengthInput.value : 14),
      width_ft: parseFloat(dom.roomWidthInput ? dom.roomWidthInput.value : 12),
      ceiling_height_ft: parseFloat(dom.roomHeightInput ? dom.roomHeightInput.value : 10),
      occupants: 3,
      has_hepa_purifier: false,
      smog_entry_risk: dom.smogRiskSelect ? dom.smogRiskSelect.value : 'HIGH'
    };

    const data = await apiFetch('/api/iaq/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!data) return;
    state.iaqData = data;

    if (dom.resRoomVolume) dom.resRoomVolume.textContent = `${data.volume_cuft.toLocaleString()} cu.ft`;
    if (dom.resTargetCadr) dom.resTargetCadr.textContent = `${data.target_cadr_cfm} CFM`;
    if (dom.resTargetAch) dom.resTargetAch.textContent = `${data.air_changes_per_hour} Changes/Hr`;

    renderPlants(data.phytoremediation_plants);
    renderHacks(data.hacks_and_precautions);
  }

  function renderPlants(plants) {
    if (!dom.plantsDisplayGrid || !plants) return;
    dom.plantsDisplayGrid.innerHTML = '';

    plants.forEach(p => {
      const card = document.createElement('div');
      card.className = 'plant-card';
      card.innerHTML = `
        <span class="plant-title">${p.name}</span>
        <span class="plant-latin">${p.scientific_name}</span>
        <span class="plant-toxin">🎯 Absorbs: ${p.primary_toxin_filtered}</span>
        <span class="plant-meta">🌱 Density: ${p.recommended_count} pots • ${p.maintenance_level}</span>
        ${p.nighttime_oxygen ? '<span class="badge-mini" style="color:#10b981;">🌙 Nighttime O₂ Generator (CAM)</span>' : ''}
      `;
      dom.plantsDisplayGrid.appendChild(card);
    });
  }

  function renderHacks(hacks) {
    if (!dom.hacksDisplayList || !hacks) return;
    dom.hacksDisplayList.innerHTML = '';

    hacks.forEach(h => {
      const item = document.createElement('div');
      item.className = 'hack-item';
      item.textContent = h;
      dom.hacksDisplayList.appendChild(item);
    });
  }

  if (dom.iaqForm) {
    dom.iaqForm.addEventListener('submit', submitIAQCalculation);
  }

  // --- 4. Quantified Impact & Sustainable Alternatives ---
  async function updateImpactEvaluation() {
    const km = parseFloat(dom.commuteKmSlider ? dom.commuteKmSlider.value : 25);
    if (dom.commuteKmLabel) dom.commuteKmLabel.textContent = `${km} km`;

    const payload = {
      daily_commute_km: km,
      commute_mode: dom.commuteModeSelect ? dom.commuteModeSelect.value : 'solo_diesel_suv',
      household_members: 4,
      winter_heating_source: 'ELECTRIC',
      cooking_style: 'HIGH_FRYING',
      adopted_ventilation_protocol: dom.chkVentProtocol ? dom.chkVentProtocol.checked : true,
      installed_diy_iaq_filter: dom.chkIaqFilter ? dom.chkIaqFilter.checked : true
    };

    const data = await apiFetch('/api/impact/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!data) return;
    state.impactData = data;

    if (dom.meterPm25Shielded) dom.meterPm25Shielded.textContent = `${data.daily_pm25_inhaled_avoided_ug.toLocaleString()} µg`;
    if (dom.meterCigsShielded) dom.meterCigsShielded.textContent = data.cigarettes_equivalent_shielded_daily;
    if (dom.meterCo2Saved) dom.meterCo2Saved.textContent = `${data.annual_co2_reduction_kg.toLocaleString()} kg`;
    if (dom.meterCarKm) dom.meterCarKm.textContent = `Equal to ${data.car_km_equivalent_saved.toLocaleString()} km not driven`;
    if (dom.meterPediatricRisk) dom.meterPediatricRisk.textContent = `${data.pediatric_lung_risk_reduction_pct}%`;
    if (dom.impactNarrativeContent) dom.impactNarrativeContent.textContent = data.explainable_impact_narrative;

    renderAlternativesTable(data.sustainable_alternatives);
  }

  function renderAlternativesTable(alts) {
    if (!dom.alternativesTableBody || !alts) return;
    dom.alternativesTableBody.innerHTML = '';

    alts.forEach(a => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><strong>${a.category}</strong></td>
        <td>${a.current}</td>
        <td><span style="color:var(--color-clean); font-weight:600;">${a.alternative}</span></td>
        <td>${a.impact}</td>
      `;
      dom.alternativesTableBody.appendChild(row);
    });
  }

  if (dom.commuteKmSlider) dom.commuteKmSlider.addEventListener('input', updateImpactEvaluation);
  if (dom.commuteModeSelect) dom.commuteModeSelect.addEventListener('change', updateImpactEvaluation);
  if (dom.chkIaqFilter) dom.chkIaqFilter.addEventListener('change', updateImpactEvaluation);
  if (dom.chkVentProtocol) dom.chkVentProtocol.addEventListener('change', updateImpactEvaluation);

  // --- 5. Community Sentinel & Grievance Generator ---
  async function submitGrievance(e) {
    if (e) e.preventDefault();

    const payload = {
      issue_type: dom.grievanceIssueSelect ? dom.grievanceIssueSelect.value : 'garbage_burning',
      ward_or_colony: dom.grievanceWardInput ? dom.grievanceWardInput.value : 'Local Ward',
      city: state.city,
      landmark: dom.grievanceLandmarkInput ? dom.grievanceLandmarkInput.value : '',
      frequency: 'DAILY_MORNING',
      impacted_residents: parseInt(dom.grievanceResidentsInput ? dom.grievanceResidentsInput.value : 850)
    };

    const data = await apiFetch('/api/community/grievance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!data) return;

    if (dom.grievancePriorityBadge) dom.grievancePriorityBadge.textContent = data.priority_tier;
    if (dom.grievanceLetterText) dom.grievanceLetterText.textContent = data.formal_grievance_letter;
    if (dom.grievanceStatutoryBasis) dom.grievanceStatutoryBasis.textContent = data.legal_statutory_basis;
    if (dom.whatsappBroadcastText) dom.whatsappBroadcastText.textContent = data.whatsapp_broadcast_message;
  }

  if (dom.grievanceForm) {
    dom.grievanceForm.addEventListener('submit', submitGrievance);
  }

  // --- Copy to Clipboard Buttons ---
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        const textToCopy = targetEl.textContent || targetEl.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
          const original = btn.textContent;
          btn.textContent = '✅ Copied!';
          setTimeout(() => { btn.textContent = original; }, 2000);
        });
      }
    });
  });

  // --- 6. GenAI Chat Assistant (Prāṇa-Mitra) ---
  async function handleChatSubmit(e) {
    if (e) e.preventDefault();
    const query = dom.chatInput ? dom.chatInput.value.trim() : '';
    if (!query) return;

    dom.chatInput.value = '';
    appendMessage('user', query);

    // Call API with deterministic fallback
    const payload = {
      message: query,
      city: state.city,
      persona: state.persona
    };

    const botMsg = appendMessage('assistant', 'Consulting Prāṇa AI specialist...');

    const res = await apiFetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res && res.reply) {
      updateMessageContent(botMsg, res.reply, res.actionable_takeaway, res.source);
    } else {
      updateMessageContent(
        botMsg,
        `For severe winter smog in ${state.city}, seal all window perimeters during the morning inversion peak (6:00 AM – 9:30 AM), rely on certified N95 masks for necessary commutes, and run mechanical IAQ purifiers continuously.`,
        'Keep homes sealed during morning inversions; ventilate strictly during midday solar peak.',
        'local_emergency_resilience_guard'
      );
    }
  }

  function appendMessage(role, text) {
    if (!dom.chatThread) return null;
    const msg = document.createElement('div');
    msg.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = role === 'assistant' ? '✦' : '👤';

    const content = document.createElement('div');
    content.className = 'msg-content';
    content.innerHTML = `<p>${text}</p>`;

    msg.appendChild(avatar);
    msg.appendChild(content);
    dom.chatThread.appendChild(msg);
    dom.chatThread.scrollTop = dom.chatThread.scrollHeight;

    return msg;
  }

  function updateMessageContent(msgEl, replyText, takeaway, source) {
    if (!msgEl) return;
    const content = msgEl.querySelector('.msg-content');
    if (!content) return;

    content.innerHTML = `
      <p>${replyText}</p>
      ${takeaway ? `<div class="msg-meta">💡 Takeaway: ${takeaway}</div>` : ''}
    `;
    dom.chatThread.scrollTop = dom.chatThread.scrollHeight;
  }

  if (dom.chatForm) {
    dom.chatForm.addEventListener('submit', handleChatSubmit);
  }

  // Prompt Chips
  dom.promptChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const prompt = chip.getAttribute('data-prompt');
      if (dom.chatInput) {
        dom.chatInput.value = prompt;
        dom.chatForm.dispatchEvent(new Event('submit'));
      }
    });
  });

  // --- Initial Data Load ---
  function refreshAllData() {
    fetchAQISnapshot();
    fetchRoutinePlan();
    submitIAQCalculation();
    updateImpactEvaluation();
  }

  refreshAllData();
});
