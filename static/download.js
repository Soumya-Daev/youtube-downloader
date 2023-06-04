document.addEventListener('DOMContentLoaded', function () {
    const loader = document.getElementById('l0ader');
    const date = new Date();
    const year = date.getFullYear();
    const dt_span = document.getElementById('_date');
    dt_span.innerHTML = year;

    var form = document.getElementById('downloadForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        loader.style.display = 'block';

        var formData = new FormData(form);

        var xhr = new XMLHttpRequest();
        xhr.open(form.method, form.action);
        xhr.responseType = 'blob';
        xhr.onload = function () {
            var filename = xhr.getResponseHeader('Content-Disposition').split('=')[1]; // exclude = and ';'
            filename = filename.replace(/"/g, '');
            filename = filename.replace(/;/g, '');
            filename = filename.replace(/filename/g, '');

            filename = decodeURIComponent(filename);
            // var type = xhr.getResponseHeader('Content-Type');
            if (xhr.status === 200) {
                var blob = xhr.response;
                var url = URL.createObjectURL(blob);
                var link = document.createElement('a');
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);

            }
            loader.style.display = 'none';
        };
        xhr.send(formData);
    });
});