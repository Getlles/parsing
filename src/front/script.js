// let form = document.getElementById('form_inp');
// let input = document.getElementById('profi');
// let vacancies = document.querySelectorAll('.object-vac');
// let nothingFoundAlert = document.querySelector('#nothingfound');
// form.addEventListener('submit', function (event) {
//     event.preventDefault();
//     let searchTerm = input.value.trim().toLowerCase();
//     let found = false;
//     vacancies.forEach(function (vacancy) {
//         let title = vacancy.querySelector('.vacs').textContent.toLowerCase();
//         if (title.includes(searchTerm)) {
//             vacancy.style.display = 'block';
//         } else {
//             vacancy.style.display = 'none';
//         }
//     });
    
//     if (!found) {
//         nothingFoundAlert.style.display = 'block';
//     } else {
//         nothingFoundAlert.style.display = 'none';
//     }
// });


// function handleFormSubmit(event) {
//     event.preventDefault(); // Предотвращаем стандартное поведение формы при отправке
//     // Получаем объект формы
//     const form = document.getElementById('form_inp');
//     // Проверяем, что пользователь ввел данные в поле поиска
//     if (!form.profi.value) {
//         alert('Пожалуйста, введите данные для поиска');
//         return;
//     }
//     // Создаем объект данных для отправки
//     const data = {
//         profi: form.profi.value
//     };
//     // Отправляем POST-запрос на сервер
//     sendDataToServer(data);
// }

// Функция для отправки данных на сервер
function sendDataToServer(user_input) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/allvac');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(user_input));

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            if (response !== 'ok') {
                alert('Ошибка сохранения');
            }
        }
    };
}
// Добавляем обработчик события отправки формы
document.getElementById('form_inp').addEventListener('submit', handleFormSubmit);

// (function() {
//     $('form').on('submit', function(e) {
//       e.preventDefault();
//       var user_input = $(this).find('[name=user_input]').val();
//       $.ajax({
//         url: '/',
//         type: 'POST',
//         data: { user_input: user_input },
//         success: function(response) {
//           // Обработка ответа от сервера
//         },
//         error: function() {
//           alert('Ошибка при отправке данных');
//         }
//       });
//     });
//   });

// function applyFilters() {
//     let vacancies = document.querySelectorAll('.object-vac');
//     let experienceFilters = Array.from(document.querySelectorAll('input[type="checkbox"][name="btn__exp"]'))
//         .filter(checkbox => checkbox.checked)
//         .map(checkbox => checkbox.value);
//     let employmentFilters = Array.from(document.querySelectorAll('input[type="checkbox"][name="bus"]'))
//         .filter(checkbox => checkbox.checked)
//         .map(checkbox => checkbox.value);

//     let nothingFound = document.getElementById('nothingfound');
//     let visibleVacancies = 0;

//     vacancies.forEach(vacancy => {
//         let experience = vacancy.getAttribute('d-exp');
//         let employment = vacancy.getAttribute('d-bus');

//         let experienceMatch = experienceFilters.length === 0 || experienceFilters.includes(experience);
//         let employmentMatch = employmentFilters.length === 0 || employmentFilters.includes(employment);

//         if (experienceMatch && employmentMatch) {
//             vacancy.style.display = 'block';
//             visibleVacancies++;
//         } else {
//             vacancy.style.display = 'none';
//         }
//     });

//     nothingFound.style.display = visibleVacancies === 0 ? 'block' : 'none';
//     console.log('Visible Vacancies:', visibleVacancies);
// }

// document.addEventListener('DOMContentLoaded', applyFilters);