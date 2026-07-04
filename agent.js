window.onload = async () => {
    debugMonitor = document.getElementById('debug-monitor');           
    const response = await fetch('http://127.0.0.1:8000/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            task: `
                1. open https://google.com/aimode
                2. then search for "'what is the meaning of life?' start your answer with '$answer: ' and end with '$end$'"
                3. parse the answer and display it on the page
            `
        })
    });
    console.log(response);
    const data = await response.json();
    debugMonitor.src = data.live_url;
}