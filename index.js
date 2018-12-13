const API = 'http://d206074b.ngrok.io'

let userId = null;

let markers = null;

let filters = null;

L.mapbox.accessToken = 'pk.eyJ1IjoiY2FybG9hYmVsbGkiLCJhIjoiY2pwZzEwNXB4MGd6YjNxbWxlcTl0dzYzbSJ9.FF55B1bVg-WK0m284jEWUw';
let map = L.mapbox.map('map', 'mapbox.streets');

onFilter();

document.getElementById('login-button').onclick = onLogin;
document.getElementById('register-button').onclick = onRegister;
document.getElementById('logout-button').onclick = onLogout;
document.getElementById('filter-button').onclick = onFilter;
document.getElementById('save-filter-button').onclick = onSaveFilter;
document.getElementById('load-filter-button').onclick = onLoadFilter;
document.getElementById('delete-filter-button').onclick = onDeleteFilter;

async function onLogin() {
    let username = document.querySelector('#login [name="username"]').value;
    let password = document.querySelector('#login [name="password"]').value;

    document.querySelector('#login [name="username"]').value = '';
    document.querySelector('#login [name="password"]').value = '';

    userId = await apiLogin(username, password);

    if (userId) {
        document.getElementById('login').style.display = 'none';

        document.getElementById('username').innerHTML = username;
        document.getElementById('logout').style.display = 'block';

        await reloadFilters();
        document.getElementById('filters').style.display = 'block';
    }
}

async function onRegister() {
    let username = document.querySelector('#login [name="username"]').value;
    let password = document.querySelector('#login [name="password"]').value;

    document.querySelector('#login [name="username"]').value = '';
    document.querySelector('#login [name="password"]').value = '';

    userId = await apiRegister(username, password);

    if (userId) {
        document.getElementById('login').style.display = 'none';

        document.getElementById('username').innerHTML = username;
        document.getElementById('logout').style.display = 'block';

        await reloadFilters();
        document.getElementById('filters').style.display = 'block';
    }
}

async function onLogout() {
    userId = null;

    document.getElementById('logout').style.display = 'none';
    document.getElementById('filters').style.display = 'none';
    document.querySelector('#user-filter [name="filter-id"]').innerHTML = '';

    document.getElementById('login').style.display = 'block';
}

async function onFilter() {
    let firstName = document.querySelector('#filter [name="first-name"]').value;
    let lastName = document.querySelector('#filter [name="last-name"]').value;
    let classYear = document.querySelector('#filter [name="class-year"]').value;
    let college = document.querySelector('#filter [name="college"]').value;
    let major = document.querySelector('#filter [name="major"]').value;
    let birthMonth = document.querySelector('#filter [name="birth-month"]').value;
    let birthDay = document.querySelector('#filter [name="birth-day"]').value;

    let filter = {
        firstName: firstName == '' ? undefined : firstName,
        lastName: lastName == '' ? undefined : lastName,
        classYear: classYear == '' ? undefined : classYear,
        college: college == ''? undefined : college,
        major: major == ''? undefined : major,
        birthMonth: birthMonth == ''? undefined : birthMonth,
        birthDay: birthDay == ''? undefined : birthDay,
    };

    let people = await apiPeople(filter);

    if (markers) {
        map.removeLayer(markers);
    }
    markers = new L.MarkerClusterGroup();
    for (let person of people) {
        let marker = L.marker([person.latitude, person.longitude]);
        marker.bindPopup(`
            <div>
                <h5>${person.firstName} ${person.lastName}</h5>
                <p>${person.college} ${person.classYear}</p>
                <p>Major: ${person.major}<p>
                <p>Birthday: ${person.birthMonth} ${person.birthDay}</p>
                <p>Room: ${person.room}</p>
            </div>
        `);
        markers.addLayer(marker);
    }
    map.addLayer(markers);
}

async function onSaveFilter() {
    let firstName = document.querySelector('#filter [name="first-name"]').value;
    let lastName = document.querySelector('#filter [name="last-name"]').value;
    let classYear = document.querySelector('#filter [name="class-year"]').value;
    let college = document.querySelector('#filter [name="college"]').value;
    let major = document.querySelector('#filter [name="major"]').value;
    let birthMonth = document.querySelector('#filter [name="birth-month"]').value;
    let birthDay = document.querySelector('#filter [name="birth-day"]').value;

    let filter = {
        firstName: firstName == '' ? undefined : firstName,
        lastName: lastName == '' ? undefined : firstName,
        classYear: classYear == ''? undefined : parseInt(classYear),
        college: college == ''? undefined : college,
        major: major == ''? undefined : major,
        birthMonth: birthMonth == ''? undefined : parseInt(birthMonth),
        birthDay: birthDay == ''? undefined : parseInt(birthDay),
    };

    await apiSaveFilter(userId, filter);

    await reloadFilters();
}

async function onLoadFilter() {
    let e = document.querySelector('#user-filter [name="filter-id"]');
    let filterId = e.options[e.selectedIndex].value;

    let filter = await apiFilter(filterId);

    document.querySelector('#filter [name="first-name"]').value = filter.firstName || '';
    document.querySelector('#filter [name="last-name"]').value = filter.lastName || '';
    document.querySelector('#filter [name="class-year"]').value = filter.classYear || '';
    document.querySelector('#filter [name="college"]').value = filter.college || '';
    document.querySelector('#filter [name="major"]').value = filter.major || '';
    document.querySelector('#filter [name="birth-month"]').value = filter.birthMonth || '';
    document.querySelector('#filter [name="birth-day"]').value = filter.birthDay || '';
}

async function onDeleteFilter() {
    let e = document.querySelector('#user-filter [name="filter-id"]');
    let filterId = e.options[e.selectedIndex].value;

    apiDeleteFilter(userId, filterId);

    await reloadFilters();
}

async function reloadFilters() {
    let e = document.querySelector('#user-filter [name="filter-id"]');
    e.innerHTML = '';
    filters = await apiFilters(userId);
    for (let filter of filters) {
        let el = document.createElement('option');
        el.value = filter.filterId;
        el.innerHTML = filter.filterId;
        e.appendChild(el);
    }
}

async function apiLogin(username, password) {
    try {
        let res = await axios.get(`${API}/login`, {
            params: {
                username,
                password,
            },
        });
        return res.data.user_id;
    } catch (e) {
        return null;
    }
}

async function apiRegister(username, password) {
    try {
        let res = await axios.post(`${API}/register`, formUrlEncoded({
            username,
            password,
        }));
        return res.data.user_id;
    } catch (e) {
        return null;
    }
}

async function apiPeople(filter) {
    try {
        let res = await axios.get(`${API}/people`, {
            params: filter,
        });
        return res.data;
    } catch (e) {
        return [];
    }
}

async function apiFilters(userId) {
    try {
        let res = await axios.get(`${API}/filter`, {
            params: {
                userId,
            },
        });
        return res.data;
    } catch (e) {
    }
}

async function apiFilter(filterId) {
    for (let filter of filters) {
        if (filter.filterId == filterId) {
            return filter;
        }
    }
    return null;
}

async function apiSaveFilter(userId, filter) {
    try {
        await axios.post(`${API}/filter`, formUrlEncoded({
            userId,
            ...filter,
        }));
    } catch (e) {
    }
}

async function apiDeleteFilter(userId, filterId) {
    try {
        await axios.post(`${API}/filterDelete`, formUrlEncoded({
            userId,
            filterId,
        }));
    } catch (e) {
    }
}

function formUrlEncoded(x) {
   return Object.keys(x).reduce((p, c) => p + (x[c] ? `&${c}=${encodeURIComponent(x[c])}` : ''), '');
}
