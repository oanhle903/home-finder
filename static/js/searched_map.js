'use strict';

// We use a function declaration for initMap because we actually *do* need
// to rely on value-hoisting in this circumstance.
function initMap() {
  const sfBayCoords = {
    lat: 37.601773,
    lng: -122.20287,
  };

  const basicMap = new google.maps.Map(document.querySelector('#map'), {
    center: sfBayCoords,
    zoom: 10,
  });

  const sfMarker = new google.maps.Marker({
    position: sfBayCoords,
    title: 'SF Bay',
    map: basicMap,
  });

  const sfInfo = new google.maps.InfoWindow({
    content: '<h1>San Francisco Bay!</h1>',
  });

  sfInfo.open(basicMap, sfMarker);
 

  const searchedData = document.querySelectorAll('.property-data');

  const markers = [];
  for (const div of searchedData) {
    console.log(div);
    const coords = {
      lat: +div.dataset.latitude,
      lng: +div.dataset.longitude,
    }
    markers.push(
      new google.maps.Marker({
        position: coords,
        title: div.dataset.address,
        map: basicMap,
      }),
    );
  }



  for (const marker of markers) {
    const markerInfo = `
      <h1>${marker.title}</h1>
      <p>
        Located at: <code>${marker.position.lat()}</code>,
        <code>${marker.position.lng()}</code>
      </p>
    `;

    const infoWindow = new google.maps.InfoWindow({
      content: markerInfo,
      maxWidth: 200,
    });

    marker.addListener('mouseover', () => {
      infoWindow.open(basicMap, marker);
    });
    marker.addListener('mouseout', () => {
      infoWindow.close();
    });
  }

}
