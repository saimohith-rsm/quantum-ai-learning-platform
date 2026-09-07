const API_BASE = import.meta.env.VITE_API_BASE || '/api';

export function getStoredToken() {
  return localStorage.getItem('quantum_token');
}

export function setStoredToken(token) {
  if (token) {
    localStorage.setItem('quantum_token', token);
  } else {
    localStorage.removeItem('quantum_token');
  }
}

function getAuthHeaders() {
  const token = getStoredToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse(resp, actionName = 'Request') {
  const contentType = resp.headers.get('content-type') || '';
  if (!contentType.includes('application/json')) {
    if (!resp.ok) {
      if (resp.status === 404) {
        throw new Error(
          `Backend endpoint not found (404). If deployed on Vercel, ensure you added environment variable VITE_API_BASE pointing to your Render backend URL (e.g. https://<your-backend>.onrender.com/api).`
        );
      }
      throw new Error(`Server returned HTTP ${resp.status} with unexpected non-JSON response.`);
    }
    // If status 200 but HTML (Vercel SPA fallback rewrite)
    throw new Error(
      `Received HTML instead of JSON. Your frontend cannot reach the backend API. Please set VITE_API_BASE in your Vercel project settings to your Render backend URL (e.g. https://<your-backend>.onrender.com/api).`
    );
  }

  const data = await resp.json();
  if (!resp.ok) {
    const errorMsg = data.detail || `${actionName} failed (HTTP ${resp.status})`;
    throw new Error(errorMsg);
  }
  return data;
}

function handleFetchError(err, actionName = 'Action') {
  if (err.name === 'TypeError' && err.message.toLowerCase().includes('fetch')) {
    throw new Error(
      `Cannot connect to backend server. If using Render free tier, the server may take ~30-50 seconds to wake up from sleep. Please wait a moment and try again.`
    );
  }
  throw err;
}

export async function loginUser(credentials) {
  try {
    const resp = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    return await handleResponse(resp, 'Login');
  } catch (err) {
    handleFetchError(err, 'Login');
  }
}

export async function registerUser(userData) {
  try {
    const resp = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return await handleResponse(resp, 'Registration');
  } catch (err) {
    handleFetchError(err, 'Registration');
  }
}

export async function demoLogin() {
  try {
    const resp = await fetch(`${API_BASE}/auth/demo-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    return await handleResponse(resp, 'Demo login');
  } catch (err) {
    handleFetchError(err, 'Demo login');
  }
}


export async function getMe(token) {
  const headers = token ? { 'Authorization': `Bearer ${token}` } : getAuthHeaders();
  const resp = await fetch(`${API_BASE}/auth/me`, { headers });
  if (!resp.ok) {
    return null;
  }
  return resp.json();
}

export async function simulateCircuit(circuit, shots = 1024, calculateSteps = true) {
  const resp = await fetch(`${API_BASE}/quantum/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ circuit, shots, calculate_steps: calculateSteps })
  });
  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.detail || 'Simulation failed');
  }
  return resp.json();
}

export async function exportQiskit(circuit) {
  const resp = await fetch(`${API_BASE}/quantum/export/qiskit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(circuit)
  });
  return resp.json();
}

export async function exportQasm(circuit) {
  const resp = await fetch(`${API_BASE}/quantum/export/qasm`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(circuit)
  });
  return resp.json();
}

export async function optimizeCircuit(circuit) {
  const resp = await fetch(`${API_BASE}/quantum/optimize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ circuit })
  });
  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.detail || 'Optimization failed');
  }
  return resp.json();
}

export async function simulateNoisyCircuit(circuit, hardwarePreset = 'ibm_eagle', customParams = {}, shots = 1024) {
  const payload = {
    circuit,
    hardware_preset: hardwarePreset,
    shots,
    ...customParams
  };
  const resp = await fetch(`${API_BASE}/quantum/simulate-noisy`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.detail || 'Noisy simulation failed');
  }
  return resp.json();
}

export async function exportMultiSdk(circuit) {
  const resp = await fetch(`${API_BASE}/quantum/export-multisdk`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ circuit })
  });
  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.detail || 'Multi-SDK export failed');
  }
  return resp.json();
}

export async function runBB84Protocol(numBits = 24, evePresent = false, eveInterceptRate = 1.0) {
  const resp = await fetch(`${API_BASE}/quantum/protocol/bb84`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      num_bits: numBits,
      eve_present: evePresent,
      eve_intercept_rate: eveInterceptRate
    })
  });
  if (!resp.ok) {
    const err = await resp.json();
    throw new Error(err.detail || 'BB84 simulation failed');
  }
  return resp.json();
}

export async function getPresets() {
  const resp = await fetch(`${API_BASE}/quantum/presets`);
  return resp.json();
}

export async function explainCircuit(circuit, userLevel = 'Beginner') {
  const resp = await fetch(`${API_BASE}/tutor/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ circuit, user_level: userLevel })
  });
  return resp.json();
}

export async function debugCircuit(circuit, goal, userLevel = 'Beginner') {
  const resp = await fetch(`${API_BASE}/tutor/debug`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ circuit, goal, user_level: userLevel })
  });
  return resp.json();
}

export async function getChallengeHint(challengeId, circuit, tier = 1) {
  const resp = await fetch(`${API_BASE}/tutor/hint`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ challenge_id: challengeId, circuit, tier })
  });
  return resp.json();
}

export async function chatWithTutor(message, circuit = null, userLevel = 'Beginner', provider = 'auto', socraticMode = false) {
  const resp = await fetch(`${API_BASE}/tutor/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      circuit,
      user_level: userLevel,
      provider,
      socratic_mode: socraticMode
    })
  });
  return resp.json();
}

export async function getCurriculumModules() {
  const resp = await fetch(`${API_BASE}/curriculum/modules`);
  return resp.json();
}

export async function getLesson(lessonId) {
  const resp = await fetch(`${API_BASE}/curriculum/lessons/${lessonId}`);
  return resp.json();
}

export async function getChallenges() {
  const resp = await fetch(`${API_BASE}/challenges`);
  return resp.json();
}

export async function submitChallenge(challengeId, circuit, userId = 1) {
  const resp = await fetch(`${API_BASE}/challenges/${challengeId}/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ challenge_id: challengeId, circuit, user_id: userId })
  });
  return resp.json();
}

export async function getSavedCircuits(userId = 1) {
  const resp = await fetch(`${API_BASE}/circuits/saved?user_id=${userId}`);
  return resp.json();
}

export async function saveCircuit(data, userId = 1) {
  const resp = await fetch(`${API_BASE}/circuits/saved?user_id=${userId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return resp.json();
}

export async function deleteSavedCircuit(circuitId, userId = 1) {
  const resp = await fetch(`${API_BASE}/circuits/saved/${circuitId}?user_id=${userId}`, {
    method: 'DELETE'
  });
  return resp.json();
}

export async function getUserProfile(userId = 1) {
  const resp = await fetch(`${API_BASE}/user/profile?user_id=${userId}`);
  return resp.json();
}

export async function recordLessonProgress(moduleId, lessonId, quizScore = 100.0, userId = 1) {
  const resp = await fetch(`${API_BASE}/user/progress`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      module_id: moduleId,
      lesson_id: lessonId,
      completed: true,
      quiz_score: quizScore
    })
  });
  return resp.json();
}
