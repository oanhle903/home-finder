"use strict";

function initialize() {
 
  const locationData = document.querySelector('#location-data');
  const lat = +locationData.dataset.latitude;
  const lng = +locationData.dataset.longitude;

  const fenway = { lat: lat, lng: lng };
  const map = new google.maps.Map(document.querySelector("#streetmap"), {
    center: fenway,
    zoom: 12, 
  });
  const panorama = new google.maps.StreetViewPanorama(
    document.querySelector("#pano"),
    {
      position: fenway,
      pov: {
        heading: 34,
        pitch: 10,
      },
    }
  );
  map.setStreetView(panorama);
}

window.initialize = initialize;
