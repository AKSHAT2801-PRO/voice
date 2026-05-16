document.getElementById('generateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const script = document.getElementById('script').value;
    const voice = document.getElementById('voice').value;
    
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = document.getElementById('spinner');
    const resultSection = document.getElementById('resultSection');
    
    // Loading State
    submitBtn.disabled = true;
    btnText.textContent = 'Generating... (This may take a minute)';
    spinner.classList.remove('hidden');
    resultSection.classList.add('hidden');
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ script, voice })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Update UI with results
            const audioPlayer = document.getElementById('audioPlayer');
            const downloadAudioBtn = document.getElementById('downloadAudioBtn');
            const downloadSubtitleBtn = document.getElementById('downloadSubtitleBtn');
            
            // Add a cache buster so browser fetches fresh file
            audioPlayer.src = data.audio_url + '?t=' + new Date().getTime();
            
            downloadAudioBtn.href = data.audio_url;
            downloadSubtitleBtn.href = data.subtitle_url;
            
            resultSection.classList.remove('hidden');
        } else {
            alert('Error generating content: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Network error or server is down. Check console.');
        console.error(error);
    } finally {
        // Reset Loading State
        submitBtn.disabled = false;
        btnText.textContent = 'Generate Studio Output';
        spinner.classList.add('hidden');
    }
});
