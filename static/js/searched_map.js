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
 

  const propertyInfo = new google.maps.InfoWindow();
  
  const searchedData = document.querySelectorAll('.property-data');

  for (const div of searchedData) {
    const property = div.dataset;

    const propertyInfoContent = `
      <div class="window-content relative flex w-72 h-24 rounded">
        <div class="relative w-1/2 h-full">
          <div class="property-thumbnail absolute h-full w-full ">
            <a href="/properties/${property.zpid}">
              <img
                class="object-cover w-full h-full"
                src="${property.img}"
                alt="houses"
              />
            </a>
          </div>
        </div>

        <div class="property-info pl-4">
          <p class="text-2xl font-semibold my-1">$${property.price}</p>
          <p class="my-1"><strong>${property.bedrooms}</strong> bds |
          <strong>${property.bathrooms}</strong> ba |
          <strong>${property.lot_area_value}</strong> ${property.lot_area_unit}
          </p>
          <p>${property.address}</p>
        </div>

      </div>
    `;

    const propertyMarker = new google.maps.Marker({
      position: {
        lat: +property.latitude,
        lng: +property.longitude,
      },
      map: basicMap, // same as saying map: map
    });

    propertyMarker.addListener('click', () => {
      propertyInfo.close();
      propertyInfo.setContent(propertyInfoContent);
      propertyInfo.open(basicMap, propertyMarker);
    });
  }
}
