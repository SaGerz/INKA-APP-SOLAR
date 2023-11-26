const [previewVid, capture, output, result] = [    
    document.getElementById('preview'),
    document.getElementById('capture'),
    document.getElementById('output'),
    document.getElementById('result'),
]

navigator.mediaDevices.getUserMedia({
    audio: false,
    video: {
        width: 400,
        height: 300,
        facingMode: "environment"
    },
}).then(stream => {
    previewVid.srcObject = stream;
    previewVid.play()
}).catch(error => {
    console.log(error)
})

capture.addEventListener('click', () => {
    const context = output.getContext('2d')

    output.width = 400;
    output.height = 300;
    
    context.drawImage(previewVid, 0, 0, output.width, output.height);
    const image = output.toDataURL("image/jpg", 0.5);

    fetch('/detect', {
        method: 'POST',
        body: JSON.stringify({image: image}),
        headers: {
            'Content-Type' : 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Periksa tipe konten respons
            const contentType = response.headers.get('content-type');
            
            if (contentType && contentType.includes('application/json')) {
                // Respons adalah JSON, parse dan kembalikan data
                return response.json();
            } else {
                // Respons bukan JSON, tanggapi sesuai kebutuhan
                throw new Error('Invalid content type in response');
            }
        } else {
            // Respons memiliki status kode HTTP yang tidak berhasil
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    })
    .then(data => {
        console.log(data)
        // Mengambil gambar hasil deteksi sebagai base64 string
        // const resultImageBase64 = data.result_image_base64;

        // Memasang base64 string ke elemen gambar 'result'
        // result.src = 'data:image/jpeg;base64,' + resultImageBase64;
        // result.src = data.result_image_path
        
        fetch('/detected_image')
        .then(response => response.blob())
        .then(blob => {
            result.src = URL.createObjectURL(blob)
        })
        .catch((error) => {
            console.log('Error : ', error)
        })
    })

})