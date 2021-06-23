// Exécute un appel AJAX GET
// Prend en paramètres l'URL cible et la fonction callback appelée en cas de succès
function ajaxGet(url, callback) {
    var req = new XMLHttpRequest();
    req.open("GET", url);
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status < 400) {
            // Appelle la fonction callback en lui passant la réponse de la requête
            callback(req.responseText);
        } else {
            console.error(req.status + " " + req.statusText + " " + url);
        }
    });
    req.addEventListener("error", function () {
        console.error("Network error with " + url);
    });
    req.send(null);
}

function ajaxLogGet($url,$arguments)
{
    var
        $http,
        $self = arguments.callee;

    if (window.XMLHttpRequest) {
        $http = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
        try {
            $http = new ActiveXObject('Msxml2.XMLHTTP');
        } catch(e) {
            $http = new ActiveXObject('Microsoft.XMLHTTP');
        }
    }

    if ($http) {
        $http.onreadystatechange = function()
        {
            if (/4|^complete$/.test($http.readyState)) {
              if (window.run_end == 0) {
                document.getElementById('ReloadThis').innerHTML = $http.responseText;
                setTimeout(function(){$self($url,$arguments);}, 1000);
              }
            }
        };
        $http.open('GET', $url, true);
        $http.send(null);
    }
}

// function sleep(ms) {
//   return new Promise(resolve => setTimeout(resolve, ms));
// }
