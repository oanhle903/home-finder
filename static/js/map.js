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

  const propertyInfo = new google.maps.InfoWindow();
 
  fetch('/properties.json')
  .then((response) => response.json())
  .then((properties) => {
    for (const property of properties) {
      const propertyInfoContent = `
        <div class="window-content relative flex w-72 h-24 rounded">
          <div class="relative w-1/2 h-full">
            <div class="property-thumbnail absolute h-full w-full ">
              <a href="/properties/${property.zpid}">
                <img
                  class="object-cover w-full h-full"
                  src="${property.img_src}"
                  alt="houses"
                />
              </a>
            </div>
          </div>

          <div class="property-info pl-4">
            <p class="text-2xl font-semibold my-1">$${property.price.toLocaleString()}</p>
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
          lat: property.latitude,
          lng: property.longitude,
        },
        title: property.address,
        map: basicMap, // same as saying map: map
      });

      propertyMarker.addListener('click', () => {
        propertyInfo.close();
        propertyInfo.setContent(propertyInfoContent);
        propertyInfo.open(basicMap, propertyMarker);
      });
    }
  })
  .catch(() => {
    alert("couldn't find");
  });

}