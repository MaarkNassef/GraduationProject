const dropArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');

let button = dropArea.querySelector('.button');
let input = dropArea.querySelector('input');

let file;

button.onclick = () => {
  input.click();
};

// when browse
input.addEventListener('change', function () {
  file = this.files[0];
  dropArea.classList.add('active');
  displayFile();
});

// when file is inside drag area
dropArea.addEventListener('dragover', (event) => {
  event.preventDefault();
  dropArea.classList.add('active');
  dragText.textContent = 'Release to Upload';
});

// when file leaves the drag area
dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('active');
  dragText.textContent = 'Drag & Drop';
});

// when file is dropped
dropArea.addEventListener('drop', (event) => {
  event.preventDefault();

  file = event.dataTransfer.files[0];
  displayFile();
});

function displayFile() {
  let fileType = file.type;

  let validExtensions = ['application/pdf'];

  if (validExtensions.includes(fileType)) {
    let fileReader = new FileReader();

    fileReader.onload = () => {
      let fileURL = fileReader.result;
      let pdfTag = `<embed src="${fileURL}" type="application/pdf" alt="pdf" pluginspage="http://www.adobe.com/products/acrobat/readstep2.html">`;
        dropArea.innerHTML = pdfTag;
    };
    fileReader.readAsDataURL(file);
  } else {
    alert('This is not a valid file type');
    dropArea.classList.remove('active');
  }
}