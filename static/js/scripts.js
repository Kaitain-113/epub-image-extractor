const removeClass = (target, _class)  => document.querySelector(target).classList.remove(_class);
    const addClass = (target, _class)  => document.querySelector(target).classList.add(_class);        
    const addText  = (target, content) => document.querySelector(target).textContent = content

    document.addEventListener('DOMContentLoaded', function() {
        const fileInput = document.getElementById('formFile');
        
        fileInput.addEventListener('change', () => {
            
            if(fileInput.files.length > 0) {
                removeClass('.submit-button', 'd-none');
                addClass('.select-an-epub', 'd-none');
                addText('.epub-file-name', fileInput.files[0].name.slice(0, 20) + '...');
                addClass('.epub-file-name', 'font-weight-bold');
                addClass('.upload-btn', 'border-3');
                addClass('.upload-btn', 'bg-success');
                removeClass('.upload-btn', 'btn-success');
            }
        });
});