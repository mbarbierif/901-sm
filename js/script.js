let alerts = [];
let videoPlayer = document.getElementById('videoPlayer');
let alertsList = document.getElementById('alertsList');
let alertsPanel = document.getElementById('alertsPanel');
let status = document.getElementById('status');
let speedControls = document.getElementById('speedControls');

function loadFiles() {
    const videoFile = document.getElementById('videoFile').files[0];
    const alertsFile = document.getElementById('alertsFile').files[0];
    
    if (!videoFile || !alertsFile) {
        alert('Please select both video and alerts files');
        return;
    }
    
    // Clear previous alerts
    alertsList.innerHTML = '';
    
    // Load video
    const videoURL = URL.createObjectURL(videoFile);
    videoPlayer.src = videoURL;
    videoPlayer.style.display = 'block';
    speedControls.style.display = 'block';
    
    // Load alerts
    const reader = new FileReader();
    reader.onload = function(e) {
        alerts = JSON.parse(e.target.result);
        alertsPanel.style.display = 'block';
        status.textContent = `Loaded ${alerts.length} alerts - Ready for monitoring`;
        setupAlertSync();
        
        // Set default speed after video is loaded
        videoPlayer.addEventListener('loadedmetadata', function() {
            setSpeed(1);
        }, { once: true });
    };
    reader.readAsText(alertsFile);
}

function setSpeed(speed) {
    if (videoPlayer.readyState >= 1) {
        // Video metadata is loaded, can set playback rate immediately
        videoPlayer.playbackRate = speed;
    } else {
        // Wait for metadata to load before setting playback rate
        videoPlayer.addEventListener('loadedmetadata', function() {
            videoPlayer.playbackRate = speed;
        }, { once: true });
    }
    
    // Update button states
    const buttons = document.querySelectorAll('.speed-controls button');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Find and highlight the active button
    buttons.forEach(btn => {
        if (btn.textContent === `${speed}x`) {
            btn.classList.add('active');
        }
    });
}

function setupAlertSync() {
    let lastCheckedTime = 0;
    
    videoPlayer.addEventListener('timeupdate', function() {
        const currentTime = videoPlayer.currentTime;
        
        // Check for new alerts since last check
        alerts.forEach(alert => {
            if (alert.timestamp > lastCheckedTime && alert.timestamp <= currentTime) {
                showAlert(alert);
            }
        });
        
        lastCheckedTime = currentTime;
    });
    
    // Reset when video restarts or seeks
    videoPlayer.addEventListener('seeked', function() {
        if (videoPlayer.currentTime < lastCheckedTime) {
            alertsList.innerHTML = '';
            lastCheckedTime = 0;
        }
    });
    
    // Clear alerts when video ends and restarts
    videoPlayer.addEventListener('ended', function() {
        alertsList.innerHTML = '';
        lastCheckedTime = 0;
    });
}

function showAlert(alert) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert-item';
    
    // Determine alert type for styling
    if (alert.alert.includes('Suspicious Activity')) {
        alertDiv.classList.add('alert-suspicious');
    } else if (alert.alert.includes('Security Alert')) {
        alertDiv.classList.add('alert-security');
    } else if (alert.alert.includes('All Clear')) {
        alertDiv.classList.add('alert-clear');
    }
    
    const timestamp = formatTime(alert.timestamp);
    alertDiv.innerHTML = `
        <span class="timestamp">[${timestamp}]</span>
        <strong>${alert.alert}</strong>
    `;
    
    // Insert at the beginning (newest first)
    alertsList.insertBefore(alertDiv, alertsList.firstChild);
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}