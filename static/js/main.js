/**
 * UrbanEase - Smart Apartment & Society Management System
 * Interactive Client Script
 */

// Web Audio API emergency alarm generator
let alarmInterval = null;
let audioCtx = null;

function playEmergencyAlarm() {
    try {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        
        if (alarmInterval) return; // Already playing
        
        let toggle = true;
        alarmInterval = setInterval(() => {
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            
            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            osc.type = 'sawtooth';
            // Alternating siren frequencies (800Hz / 1200Hz)
            osc.frequency.setValueAtTime(toggle ? 880 : 1200, audioCtx.currentTime);
            
            gainNode.gain.setValueAtTime(0.05, audioCtx.currentTime); // Low volume so it doesn't blast
            gainNode.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.4);
            
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 0.5);
            
            toggle = !toggle;
        }, 500);
    } catch (e) {
        console.error("Audio Context not supported or allowed by browser policy.", e);
    }
}

function stopEmergencyAlarm() {
    if (alarmInterval) {
        clearInterval(alarmInterval);
        alarmInterval = null;
    }
}

function startRealtimeClock() {
    const clock = document.getElementById("current-time");
    if (!clock) return;

    const formatter = new Intl.DateTimeFormat("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true
    });

    const updateClock = () => {
        clock.textContent = formatter.format(new Date()).toUpperCase();
    };

    updateClock();
    setInterval(updateClock, 1000);
}

// Attach listeners on load
document.addEventListener("DOMContentLoaded", () => {
    startRealtimeClock();

    // If there is an active emergency alert element on the page, trigger alarm!
    const activeEmergencies = document.querySelectorAll(".alert-banner-emergency");
    if (activeEmergencies.length > 0) {
        // Play siren sound. To comply with browser autoplays, we will trigger it on the first click.
        document.body.addEventListener('click', () => {
            playEmergencyAlarm();
        }, { once: true });
        
        // Add a button to stop the alarm
        activeEmergencies.forEach(banner => {
            const stopBtn = document.createElement("button");
            stopBtn.className = "btn btn-sm btn-outline-danger ms-3 border-0";
            stopBtn.innerHTML = "<i class='fas fa-volume-mute'></i> Mute Siren";
            stopBtn.onclick = (e) => {
                e.stopPropagation();
                stopEmergencyAlarm();
                stopBtn.innerHTML = "<i class='fas fa-volume-off'></i> Siren Muted";
                stopBtn.disabled = true;
            };
            banner.appendChild(stopBtn);
        });
    }

    // Auto-dismiss standard alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll(".alert:not(.alert-banner-emergency)");
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});
