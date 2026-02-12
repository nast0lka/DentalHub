const serviceSelect = document.getElementById("service_id");
const doctorSelect = document.getElementById("doctor_id");
const dateInput = document.getElementById("date");
const timeSelect = document.getElementById("time");

const WORK_HOURS = Array.from({length: 10}, (_, i) => `${9 + i}:00`.padStart(5, "0"));

serviceSelect.addEventListener("change", async () => {
    const specId = serviceSelect.selectedOptions[0].dataset.spec;

    doctorSelect.innerHTML = `<option disabled selected>Загрузка...</option>`;
    doctorSelect.disabled = true;

    const res = await fetch(`/doctors/by-specialization/${specId}`);
    const doctors = await res.json();

    doctorSelect.innerHTML = `<option disabled selected>Выберите врача</option>`;
    doctors.forEach(d => {
        doctorSelect.innerHTML += `<option value="${d.id}">${d.name}</option>`;
    });

    doctorSelect.disabled = false;
});

doctorSelect.addEventListener("change", () => {
    dateInput.disabled = false;
});

dateInput.addEventListener("change", async () => {
    const doctorId = doctorSelect.value;
    const date = dateInput.value;

    timeSelect.innerHTML = `<option disabled selected>Загрузка...</option>`;
    timeSelect.disabled = true;

    const res = await fetch(`/doctors/${doctorId}/occupied-slots?date=${date}`);
    const occupied = await res.json();

    const available = WORK_HOURS.filter(h => !occupied.includes(h));

    timeSelect.innerHTML = `<option disabled selected>Выберите время</option>`;
    available.forEach(t => {
        timeSelect.innerHTML += `<option value="${t}">${t}</option>`;
    });

    timeSelect.disabled = false;
});

