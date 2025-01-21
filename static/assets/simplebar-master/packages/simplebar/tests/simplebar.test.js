import SimpleBar from '../src';

beforeEach(() => {
  jest.resetModules();

  // Set up our document body
  document.body.innerHTML =
    '<div id="simplebar" data-simplebar-auto-hide="true"></div>';
});

test('should call constructor', () => {
  const SimpleBar = require('../src/simplebar').default;
  jest.mock('../src/simplebar');

  new SimpleBar(document.getElementById('simplebar'));

  expect(SimpleBar).toHaveBeenCalledTimes(1);
});

test('should return the content element', () => {
  const simpleBar = new SimpleBar(document.getElementById('simplebar'));
  const contentElement = simpleBar.getContentElement();

  expect(contentElement).toBe(simpleBar.contentEl);
});

test('should return the scroll element', () => {
  const simpleBar = new SimpleBar(document.getElementById('simplebar'));
  const scrollElement = simpleBar.getScrollElement();

  expect(scrollElement).toBe(simpleBar.contentWrapperEl);
});

test('should unmount SimpleBar', () => {
  const simpleBar = new SimpleBar(document.getElementById('simplebar'));

  simpleBar.unMount();

  expect(SimpleBar.instances.get(simpleBar.el)).toBeUndefined();
});

test('should return the element options', () => {
  const simpleBar = new SimpleBar(document.getElementById('simplebar'));

  expect(SimpleBar.getOptions(simpleBar.el.attributes)).toEqual({
    autoHide: true
  });
});

test('mouse should be within bounds', () => {
  const simpleBar = new SimpleBar(document.getElementById('simplebar'));

  simpleBar.mouseX = 20;
  simpleBar.mouseY = 20;

  const isWithinBounds = simpleBar.isWithinBounds({
    bottom: 110,
    height: 100,
    left: 10,
    right: 110,
    top: 10,
    width: 100,
    x: 10,
    y: 10
  });

  expect(isWithinBounds).toBeTruthy();
});

test('onPointerEvent listener should be unsubscribed on unmount', () => {
  const element = document.getElementById('simplebar');
  const init = SimpleBar.prototype.init;

  SimpleBar.prototype.init = () => {};

  const simpleBar = new SimpleBar(element);

  simpleBar.init = init;

  jest.spyOn(simpleBar, 'onPointerEvent');

  simpleBar.init();

  simpleBar.unMount();

  element.dispatchEvent(new MouseEvent('mousedown'));

  expect(simpleBar.onPointerEvent).not.toHaveBeenCalled();
});
