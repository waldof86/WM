return (function() {
var jobs = [];
var els = document.getElementById(
    'experience-section').getElementsByTagName('ul')[0].getElementsByTagName('li');
for (var i = 0; i < els.length; i++) {
    if (els[i].className != 'pv-entity__position-group-role-item-fading-timeline') {
        if (els[i].getElementsByClassName('pv-entity__position-group-role-item-fading-timeline').length > 0) {} else {
            try {
                position = els[i].getElementsByClassName(
                    'pv-entity__summary-info')[0].getElementsByTagName('h3')[0].innerText;
            } catch (err) {
                position = '';
            }
            try {
                company_name = els[i].getElementsByClassName(
                    'pv-entity__summary-info')[0].getElementsByClassName('pv-entity__secondary-title')[0].innerText;
            } catch (err) {
                company_name = '';
            }
            try {
                date_ranges = els[
                    i].getElementsByClassName('pv-entity__summary-info')[0].getElementsByClassName(
                    'pv-entity__date-range')[0].getElementsByTagName('span')[1].innerText;
            } catch (err) {
                date_ranges = '';
            }
            try {
                job_location = els[i].getElementsByClassName(
                    'pv-entity__summary-info')[0].getElementsByClassName('pv-entity__location')[0].getElementsByTagName(
                    'span')[1].innerText;
            } catch (err) {
                job_location = '';
            }
            try {
                company_url =
                    els[i].getElementsByTagName('a')[0].href;
            } catch (err) {
                company_url = '';
            }
            jobs.push(
                [position, company_name, company_url, date_ranges, job_location]);
        }
    }
}
return jobs;
})();)