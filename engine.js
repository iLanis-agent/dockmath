(function (root) {
  "use strict";
  var DECK_KG = 30;    // labeled decking weight, kg per m2
  var PERSON_KG = 90;  // labeled person, kg
  var DRUM_KG = 180;   // labeled lift per float drum, kg
  var FREEBOARD = 0.6; // labeled freeboard above water, m
  var EMBED = 1.0;     // labeled pile embedment, m
  var GANG_SLOPE = 3;  // labeled gangway run per unit drop

  function round1(x) { return Math.round(x * 10) / 10; }
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }

  function floatPlan(deckWm, deckLm, people) {
    if (!(deckWm > 0) || !(deckLm > 0) || !(people >= 0)) return { error: "the deck sides must be positive and the people zero or more" };
    var area = round1(deckWm * deckLm);
    var load = round1(area * DECK_KG + people * PERSON_KG);
    var drums = Math.max(2, Math.ceil(load / DRUM_KG));
    var verdict;
    if (load <= 500) verdict = "a light dock";
    else if (load <= 1500) verdict = "a family dock";
    else verdict = "a party dock";
    return { area: area, load: load, drums: drums, verdict: verdict };
  }

  function pilePlan(depthM) {
    if (!(depthM > 0)) return { error: "the water depth must be positive" };
    var pile = round1(depthM + FREEBOARD + EMBED);
    var verdict;
    if (depthM <= 1.5) verdict = "shallow water";
    else if (depthM <= 3) verdict = "a normal shore";
    else verdict = "deep water";
    return { pile: pile, verdict: verdict };
  }

  function gangPlan(dropM) {
    if (!(dropM > 0)) return { error: "the bank drop must be positive" };
    var length = round1(dropM * GANG_SLOPE);
    var verdict;
    if (dropM <= 0.3) verdict = "nearly level";
    else if (dropM <= 1) verdict = "an easy slope";
    else verdict = "a steep drop";
    return { length: length, verdict: verdict };
  }

  function renderFloat(r, deckWm, deckLm, people) {
    return "A deck " + deckWm + " m by " + deckLm + " m is " + r.area + " m2 and a labeled " + r.load
      + " kg with " + plural(people, "person", "people") + " - " + plural(r.drums, "drum") + ", " + r.verdict + ".";
  }

  function renderPile(r, depthM) {
    return "Water " + depthM + " m deep asks piles " + r.pile + " m long with a labeled "
      + FREEBOARD + " m freeboard - " + r.verdict + ".";
  }

  function renderGang(r, dropM) {
    return "A bank " + dropM + " m above the dock at a labeled 1:" + GANG_SLOPE + " slope asks a gangway "
      + r.length + " m long - " + r.verdict + ".";
  }

  var api = { floatPlan: floatPlan, pilePlan: pilePlan, gangPlan: gangPlan, renderFloat: renderFloat, renderPile: renderPile, renderGang: renderGang };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.DockMath = api;
})(this);
