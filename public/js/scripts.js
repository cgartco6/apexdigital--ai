// Create AI particles
document.addEventListener('DOMContentLoaded', function() {
    const particleContainer = document.getElementById('aiParticles');
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.classList.add('ai-particle');
        
        const size = Math.random() * 100 + 10;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        
        particle.style.animationDuration = `${Math.random() * 30 + 10}s`;
        
        particleContainer.appendChild(particle);
    }
    
    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Sticky navbar
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        navbar.classList.toggle('shadow-sm', window.scrollY > 50);
    });
    
    // Update stats animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                updateStats();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    observer.observe(document.querySelector('.stats-banner'));
    
    function updateStats() {
        const stats = document.querySelectorAll('.stats-banner h2');
        stats.forEach(stat => {
            const target = parseInt(stat.textContent);
            let current = 0;
            const increment = target / 100;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    clearInterval(timer);
                    stat.textContent = target;
                } else {
                    stat.textContent = Math.round(current);
                }
            }, 20);
        });
    }
});
